import re
from serpapi import GoogleSearch
import config


def _normalize_phone(raw: str) -> str | None:
    digits = re.sub(r"\D", "", raw)
    # strip leading country code if already present
    if digits.startswith(config.COUNTRY_CODE):
        digits = digits[len(config.COUNTRY_CODE):]
    # strip leading 0 (UK local format)
    if digits.startswith("0"):
        digits = digits[1:]
    if len(digits) == 10:
        return f"+{config.COUNTRY_CODE}{digits}"
    return None


def scrape_leads() -> list[dict]:
    query = f"{config.CATEGORY} {config.LOCATION}"
    leads: list[dict] = []

    for page in range(config.SCRAPE_PAGES):
        params = {
            "engine": "google_maps",
            "q": query,
            "type": "search",
            "start": page * 20,
            "api_key": config.SERPAPI_KEY,
        }
        results = GoogleSearch(params).get_dict()
        local_results = results.get("local_results", [])

        if not local_results:
            break

        for place in local_results:
            # skip businesses that already have a website
            if place.get("website"):
                continue

            raw_phone = place.get("phone", "").strip()
            if not raw_phone:
                continue

            phone = _normalize_phone(raw_phone)
            if not phone:
                continue

            leads.append({
                "name": place.get("title", "").strip(),
                "phone": phone,
                "category": place.get("type", config.CATEGORY),
            })

    return leads
