# outreach-tool

Automated local business outreach: finds businesses with no website on Google Maps and sends them an SMS.

## How it works

- Queries Google Maps via SerpAPI for local businesses in a target area
- Filters results to businesses with no website listed
- Stores leads in a local SQLite database (`leads.db`)
- Sends SMS messages via Twilio on a daily schedule

## Setup

```bash
git clone https://github.com/tobilobasalawu/outreach-tool.git
cd outreach-tool
pip install -r requirements.txt
cp .env.example .env
```

Fill in your credentials in `.env` before running anything.

## Getting your SerpAPI key

1. Go to [serpapi.com](https://serpapi.com) and sign up for an account
2. After signing in, go to your dashboard
3. Your API key is listed under **API Key** — copy it
4. Add it to `.env` as `SERPAPI_KEY=your_key_here`

## Getting your Twilio credentials

1. Sign up at [twilio.com](https://twilio.com)
2. Go to the Console — your **Account SID** and **Auth Token** are shown under **Account Info**
3. Add them to `.env`:
   ```
   TWILIO_SID=your_account_sid
   TWILIO_TOKEN=your_auth_token
   ```
4. Register an Alphanumeric Sender ID (required for UK SMS):
   - Go to Console → Messaging → Senders → Alphanumeric Sender IDs
   - Click **Register an Alphanumeric Sender ID**
   - Choose a name: max 11 characters, letters and numbers only, no spaces (e.g. `WebRedesign`)
   - Complete the UK registration form — usually approved within a few hours
   - Set it in `.env`:
     ```
     TWILIO_FROM_NUMBER=WebRedesign
     ```
   - Note: recipients see your sender name instead of a phone number and cannot reply

> **SMS pricing:** Sending to UK numbers costs approximately £0.04/message. Check [twilio.com/sms/pricing](https://www.twilio.com/sms/pricing) for current rates. No opt-ins or template approvals required.

## Usage

**Manual scrape — find leads now:**
```bash
python -c "import db; db.init_db(); from main import scrape_now; scrape_now()"
```

**Run the scheduler — sends a batch of 5 leads daily at 09:00:**
```bash
python main.py
```

**Inspect stored leads:**
```bash
sqlite3 leads.db "SELECT * FROM leads LIMIT 10;"
```
