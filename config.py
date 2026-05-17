import os
from dotenv import load_dotenv

load_dotenv()

SERPAPI_KEY: str = os.environ["SERPAPI_KEY"]
TWILIO_SID: str = os.environ["TWILIO_SID"]
TWILIO_TOKEN: str = os.environ["TWILIO_TOKEN"]
TWILIO_FROM_NUMBER: str = os.environ["TWILIO_FROM_NUMBER"]
LOCATION: str = os.environ["LOCATION"]
CATEGORY: str = os.environ["CATEGORY"]
COUNTRY_CODE: str = os.getenv("COUNTRY_CODE", "44")
SCRAPE_PAGES: int = int(os.getenv("SCRAPE_PAGES", "3"))
