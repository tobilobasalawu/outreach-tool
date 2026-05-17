import time
import schedule
import db
import scraper
import messenger


def scrape_now() -> None:
    leads = scraper.scrape_leads()
    inserted = 0
    for lead in leads:
        if db.insert_lead(lead["name"], lead["phone"], lead["category"]):
            inserted += 1
    print(f"[scrape] {len(leads)} found, {inserted} new leads added to DB")


def send_daily_batch() -> None:
    leads = db.get_unsent_leads(limit=5)
    if not leads:
        print("[batch] no unsent leads")
        return

    for lead in leads:
        success = messenger.send_whatsapp(lead["name"], lead["phone"])
        if success:
            db.mark_messaged(lead["phone"])
            print(f"[batch] messaged {lead['name']} ({lead['phone']})")


if __name__ == "__main__":
    db.init_db()
    schedule.every().day.at("09:00").do(send_daily_batch)
    print("[main] scheduler running — daily batch at 09:00")

    while True:
        schedule.run_pending()
        time.sleep(60)
