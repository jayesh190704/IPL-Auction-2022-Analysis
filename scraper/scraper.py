from __future__ import annotations

import csv
import re
from datetime import date, datetime
from pathlib import Path
from typing import Any
from urllib.parse import quote_plus, urlparse

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


AUCTION_YEAR = 2022
AUCTION_DATE = date(2022, 2, 12)
AUCTION_URL = f"https://www.iplt20.com/auction/{AUCTION_YEAR}"
WAIT_TIMEOUT_SECONDS = 30
OUTPUT_FILE = Path(__file__).resolve().parents[1] / "raw_data" / "players_raw.csv"

OUTPUT_COLUMNS = [
    "Auction Year",
    "Auction Date",
    "Status",
    "Team",
    "Team Slug",
    "Sr No",
    "Player Name",
    "Player Profile URL",
    "Search URL",
    "Country",
    "Role",
    "Specialization",
    "Base Price",
    "Sold Price",
    "Capped Status",
    "Is Overseas",
    "IPL Debut",
    "Date of Birth",
    "Age",
    "Matches",
    "Batting Style",
    "Bowling Style",
    "About",
    "Auction Source URL",
]


def build_driver() -> webdriver.Chrome:
    """Create a Chrome WebDriver configured for stable scraping."""
    options = ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")
    return webdriver.Chrome(service=Service(), options=options)


def clean_text(text: str) -> str:
    """Normalize whitespace from visible page text."""
    return " ".join(text.replace("\n", " ").replace("\xa0", " ").split())


def slugify(text: str) -> str:
    """Convert a string into a URL-friendly slug for loose matching."""
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def normalize_price(value: str) -> str:
    """Store prices with a rupee prefix when the row uses numeric cells."""
    cleaned = clean_text(value)
    if not cleaned:
        return ""
    if cleaned.startswith("₹"):
        return cleaned
    return f"₹{cleaned}"


def parse_date_of_birth(value: str) -> date | None:
    """Parse IPL profile dates such as '05 February 1999'."""
    cleaned = clean_text(value)
    if not cleaned or cleaned in {"0", "N/A", "-"}:
        return None
    try:
        return datetime.strptime(cleaned, "%d %B %Y").date()
    except ValueError:
        return None


def calculate_age(dob: date | None, reference_date: date) -> str:
    """Calculate player age on the auction date."""
    if dob is None:
        return ""
    years = reference_date.year - dob.year
    if (reference_date.month, reference_date.day) < (dob.month, dob.day):
        years -= 1
    return str(years)


def get_team_slug(table: WebElement) -> str:
    """Read the team slug from the sold-player table id."""
    table_id = table.get_attribute("id") or ""
    return table_id.removeprefix("t3-")


def get_team_name(table: WebElement) -> str:
    """Derive a readable team name from the table id."""
    return get_team_slug(table).replace("-", " ").title()


def wait_for_auction_page(driver: webdriver.Chrome) -> None:
    """Open the auction page and wait until sold-player tables are present."""
    driver.get(AUCTION_URL)
    wait = WebDriverWait(driver, WAIT_TIMEOUT_SECONDS)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table.sold-players")))


def extract_auction_rows(driver: webdriver.Chrome) -> list[dict[str, str]]:
    """Scrape sold-player rows from all team tables on the auction page."""
    wait_for_auction_page(driver)
    tables = driver.find_elements(By.CSS_SELECTOR, "table.sold-players")
    rows: list[dict[str, str]] = []

    for table in tables:
        team_name = get_team_name(table)
        team_slug = get_team_slug(table)
        body_rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")

        for row in body_rows:
            cells = row.find_elements(By.CSS_SELECTOR, "td")
            if len(cells) < 5:
                continue

            player_name = clean_text(cells[1].text)
            if not player_name:
                continue

            row_data = {
                "Auction Year": str(AUCTION_YEAR),
                "Auction Date": AUCTION_DATE.isoformat(),
                "Status": "Sold",
                "Team": team_name,
                "Team Slug": team_slug,
                "Sr No": clean_text(cells[0].text),
                "Player Name": player_name,
                "Player Profile URL": "",
                "Search URL": "",
                "Country": "",
                "Role": "",
                "Specialization": "",
                "Base Price": normalize_price(cells[2].text),
                "Sold Price": normalize_price(cells[3].text),
                "Capped Status": clean_text(cells[4].text),
                "Is Overseas": "Yes" if cells[1].find_elements(By.TAG_NAME, "img") else "No",
                "IPL Debut": "",
                "Date of Birth": "",
                "Age": "",
                "Matches": "",
                "Batting Style": "",
                "Bowling Style": "",
                "About": "",
                "Auction Source URL": AUCTION_URL,
            }
            rows.append(row_data)

    return rows


def get_label_value_from_lines(lines: list[str], label: str) -> str:
    """Find the visible value that appears immediately before a label."""
    try:
        label_index = lines.index(label)
    except ValueError:
        return ""

    if label_index == 0:
        return ""
    return lines[label_index - 1]


def extract_profile_table_details(driver: webdriver.Chrome) -> dict[str, str]:
    """Parse structured fields from tables on the player page when available."""
    details: dict[str, str] = {}
    table_rows = driver.find_elements(By.CSS_SELECTOR, "table tr")

    for row in table_rows:
        cells = [clean_text(cell.text) for cell in row.find_elements(By.CSS_SELECTOR, "th,td")]
        cells = [cell for cell in cells if cell]
        if not cells:
            continue

        if len(cells) >= 4 and cells[0].lower() == "role" and cells[2].lower() == "nationality":
            details["Role"] = cells[1]
            details["Country"] = cells[3]
            continue

        if len(cells) >= 4 and cells[0].lower() == "bats" and cells[2].lower() == "bowls":
            details["Batting Style"] = cells[1]
            details["Bowling Style"] = cells[3]
            continue

        if len(cells) >= 2 and cells[0].lower() == "bats":
            details["Batting Style"] = cells[1]
            continue

        if len(cells) >= 2 and cells[0].lower() == "bowls":
            details["Bowling Style"] = cells[1]
            continue

    return details


def extract_profile_details(driver: webdriver.Chrome) -> dict[str, str]:
    """Collect rich metadata from an IPL player profile page."""
    wait = WebDriverWait(driver, WAIT_TIMEOUT_SECONDS)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    body_text = driver.find_element(By.TAG_NAME, "body").text
    lines = [clean_text(line) for line in body_text.splitlines() if clean_text(line)]
    details = extract_profile_table_details(driver)

    if lines:
        details.setdefault("Player Name", lines[0])
    if len(lines) > 1:
        details.setdefault("Country", lines[1])

    details.setdefault("IPL Debut", get_label_value_from_lines(lines, "IPL Debut"))
    details.setdefault("Specialization", get_label_value_from_lines(lines, "Specialization"))
    details.setdefault("Date of Birth", get_label_value_from_lines(lines, "Date of Birth"))
    details.setdefault("Matches", get_label_value_from_lines(lines, "Matches"))

    about_text = ""
    if "About" in lines:
        about_index = lines.index("About")
        stop_labels = {"Batting & Fielding Stats", "Bowling", "Player Details", "Rest Of the Squad"}
        about_lines: list[str] = []
        for line in lines[about_index + 1 :]:
            if line in stop_labels:
                break
            about_lines.append(line)
        about_text = clean_text(" ".join(about_lines))
    details["About"] = about_text

    return details


def score_candidate_url(player_name: str, candidate_url: str, candidate_text: str) -> tuple[int, int]:
    """Rank potential player URLs returned from the IPL search page."""
    player_slug = slugify(player_name)
    parsed_path = urlparse(candidate_url).path.strip("/")
    path_parts = parsed_path.split("/")
    candidate_slug = path_parts[1] if len(path_parts) >= 2 else ""
    candidate_text_slug = slugify(candidate_text)

    score = 0
    if candidate_slug == player_slug:
        score += 100
    elif player_slug and player_slug in candidate_slug:
        score += 70

    if candidate_text_slug == player_slug:
        score += 50
    elif player_slug and player_slug in candidate_text_slug:
        score += 25

    return score, len(candidate_url)


def resolve_player_profile_url(driver: webdriver.Chrome, player_name: str) -> tuple[str, str]:
    """Search the IPL site and return the best matching player profile URL."""
    search_url = f"https://www.iplt20.com/search?type=all&text={quote_plus(player_name)}"
    driver.get(search_url)

    wait = WebDriverWait(driver, WAIT_TIMEOUT_SECONDS)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    anchors = driver.find_elements(By.CSS_SELECTOR, "a[href*='/players/']")
    candidates: list[tuple[tuple[int, int], str]] = []

    for anchor in anchors:
        href = anchor.get_attribute("href") or ""
        if "/players/" not in href:
            continue
        anchor_text = clean_text(anchor.text)
        rank = score_candidate_url(player_name, href, anchor_text)
        if rank[0] > 0:
            candidates.append((rank, href))

    if not candidates:
        return "", search_url

    candidates.sort(key=lambda item: item[0], reverse=True)
    return candidates[0][1], search_url


def enrich_with_profiles(
    driver: webdriver.Chrome, auction_rows: list[dict[str, str]]
) -> list[dict[str, str]]:
    """Resolve player profiles and merge richer metadata into auction rows."""
    profile_cache: dict[str, dict[str, str]] = {}
    url_cache: dict[str, tuple[str, str]] = {}
    enriched_rows: list[dict[str, str]] = []

    for row in auction_rows:
        player_name = row["Player Name"]

        if player_name not in url_cache:
            url_cache[player_name] = resolve_player_profile_url(driver, player_name)

        profile_url, search_url = url_cache[player_name]
        row["Player Profile URL"] = profile_url
        row["Search URL"] = search_url

        if profile_url and profile_url not in profile_cache:
            driver.get(profile_url)
            profile_cache[profile_url] = extract_profile_details(driver)

        profile_details = profile_cache.get(profile_url, {})

        row["Country"] = profile_details.get("Country", row["Country"])
        row["Role"] = profile_details.get("Role") or profile_details.get("Specialization", row["Role"])
        row["Specialization"] = profile_details.get("Specialization", row["Specialization"])
        row["IPL Debut"] = profile_details.get("IPL Debut", row["IPL Debut"])
        row["Date of Birth"] = profile_details.get("Date of Birth", row["Date of Birth"])
        row["Matches"] = profile_details.get("Matches", row["Matches"])
        row["Batting Style"] = profile_details.get("Batting Style", row["Batting Style"])
        row["Bowling Style"] = profile_details.get("Bowling Style", row["Bowling Style"])
        row["About"] = profile_details.get("About", row["About"])

        dob = parse_date_of_birth(row["Date of Birth"])
        row["Age"] = calculate_age(dob, AUCTION_DATE)

        if not row["Country"] and row["Is Overseas"] == "No":
            row["Country"] = "Indian"

        enriched_rows.append(row)

    return enriched_rows


def sanitize_rows(rows: list[dict[str, Any]]) -> list[dict[str, str]]:
    """Project rows into a stable CSV schema."""
    sanitized_rows: list[dict[str, str]] = []
    for row in rows:
        sanitized_row = {column: clean_text(str(row.get(column, ""))) for column in OUTPUT_COLUMNS}
        sanitized_rows.append(sanitized_row)
    return sanitized_rows


def scrape_players() -> list[dict[str, str]]:
    """Collect sold-player data and enrich it with profile information."""
    driver = build_driver()

    try:
        auction_rows = extract_auction_rows(driver)
        if not auction_rows:
            raise RuntimeError("No sold-player rows were scraped from the IPL auction page.")
        enriched_rows = enrich_with_profiles(driver, auction_rows)
        return sanitize_rows(enriched_rows)
    except TimeoutException as exc:
        raise RuntimeError(
            "Timed out while waiting for IPL auction or player profile content to load."
        ) from exc
    finally:
        driver.quit()


def write_csv(rows: list[dict[str, str]], output_file: Path) -> None:
    """Write scraped rows to the raw data directory."""
    if not rows:
        raise RuntimeError("No sold-player rows were scraped from the IPL auction page.")

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    rows = scrape_players()
    write_csv(rows, OUTPUT_FILE)
    print(f"Saved {len(rows)} records to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
