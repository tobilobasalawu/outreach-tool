# outreach-tool

Automated local business outreach: finds businesses with no website on Google Maps and sends them a WhatsApp message.

## How it works

- Queries Google Maps via SerpAPI for local businesses in a target area
- Filters results to businesses with no website listed
- Stores leads in a local SQLite database (`leads.db`)
- Sends WhatsApp messages via Twilio on a daily schedule

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
   TWILIO_ACCOUNT_SID=your_account_sid
   TWILIO_AUTH_TOKEN=your_auth_token
   ```
4. For the WhatsApp sender number:
   - **Sandbox (testing):** Go to Messaging → Try it out → Send a WhatsApp message. Use the sandbox number and set:
     ```
     TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
     ```
     Sandbox only works with numbers that have opted in by messaging the sandbox join code.
   - **Production:** Apply for an approved WhatsApp Business sender at [twilio.com/whatsapp/request-access](https://www.twilio.com/whatsapp/request-access). Once approved, set `TWILIO_WHATSAPP_FROM` to your approved number in `whatsapp:+1xxxxxxxxxx` format.

> **Warning:** The WhatsApp Business API requires Meta-approved message templates for cold outreach. You cannot send free-form messages to users who have not messaged you first. Sandbox mode only works with numbers that have explicitly opted in.

## Usage

**Manual scrape — find leads now:**
```bash
python -c "import db; db.init_db(); from main import scrape_now; scrape_now()"
```

**Run the scheduler — scrape and send on a daily schedule:**
```bash
python main.py
```

**Inspect stored leads:**
```bash
sqlite3 leads.db "SELECT * FROM leads LIMIT 10;"
```
