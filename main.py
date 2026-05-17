import argparse
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


def send_daily_batch(limit: int = 5, dry_run: bool = False) -> None:
    leads = db.get_unsent_leads(limit=limit)
    if not leads:
        print("[batch] no unsent leads")
        return

    for lead in leads:
        success = messenger.send_whatsapp(lead["name"], lead["phone"], dry_run=dry_run)
        if success and not dry_run:
            db.mark_messaged(lead["phone"])
            print(f"[batch] messaged {lead['name']} ({lead['phone']})")
        elif success and dry_run:
            print(f"[batch] DRY RUN — would message {lead['name']} ({lead['phone']})")


def run_scheduler() -> None:
    db.init_db()
    schedule.every().day.at("09:00").do(send_daily_batch)
    print("[main] scheduler running — daily batch at 09:00")

    while True:
        schedule.run_pending()
        time.sleep(60)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="main.py",
        description="Outreach tool — scrape no-website businesses and send WhatsApp messages.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # scrape command
    sub.add_parser("scrape", help="Scrape Google Maps and store new leads in the DB.")

    # send command
    send_p = sub.add_parser("send", help="Send WhatsApp messages to unsent leads.")
    send_p.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Max number of leads to message in one batch (default: 5).",
    )
    send_p.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview messages without actually sending them.",
    )

    # run command (scheduler)
    sub.add_parser("run", help="Start the scheduler (sends daily batch at 09:00).")

    return parser


if __name__ == "__main__":
    db.init_db()
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "scrape":
        scrape_now()
    elif args.command == "send":
        send_daily_batch(limit=args.limit, dry_run=args.dry_run)
    elif args.command == "run":
        run_scheduler()
