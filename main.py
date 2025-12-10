# ============================================================
#  AI Lead Follow-Up System - main.py (FULL WITH LOGGING)
# ============================================================

import os
import time
import json
import requests
import smtplib
import gspread
from email.message import EmailMessage
from datetime import date
from dateutil import parser as dtparser
from dotenv import load_dotenv
import logging

from config import (
    SPREADSHEET_ID, SHEET_NAME,
    GMAIL_FROM, GMAIL_APP_PASSWORD, FROM_NAME, DEFAULT_SUBJECT,
    OLLAMA_HOST, OLLAMA_MODEL,
    OPENROUTER_API_KEY, OPENROUTER_URL
)

load_dotenv()

# ------------------------------------------------------------
# LOGGING SETUP
# ------------------------------------------------------------
logging.basicConfig(
    filename="logs/ai_followup.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("=== Follow-Up Bot Loaded ===")

# ------------------------------------------------------------
# GOOGLE SHEETS CONNECTION
# ------------------------------------------------------------
def connect_sheets(path="credentials/google-service-account.json"):
    try:
        gc = gspread.service_account(filename=path)
        sh = gc.open_by_key(SPREADSHEET_ID)
        ws = sh.worksheet(SHEET_NAME)
        logging.info("Connected to Google Sheet successfully.")
        return ws
    except Exception as e:
        logging.exception("FAILED to connect to Google Sheets!")
        raise e


# ------------------------------------------------------------
# SEND EMAIL (SMTP)
# ------------------------------------------------------------
def send_email(to_email, subject, html):
    msg = EmailMessage()
    msg["From"] = f"{FROM_NAME} <{GMAIL_FROM}>"
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(html, subtype="html")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(GMAIL_FROM, GMAIL_APP_PASSWORD)
        smtp.send_message(msg)


# ------------------------------------------------------------
# OLLAMA STREAMING RESPONSE
# ------------------------------------------------------------
def ask_ollama(prompt):
    logging.info("Sending prompt to Ollama...")
    try:
        url = f"{OLLAMA_HOST}/api/generate"
        payload = {"model": OLLAMA_MODEL, "prompt": prompt}

        response = requests.post(url, json=payload, stream=True)
        response.raise_for_status()

        full = ""
        for line in response.iter_lines(decode_unicode=True):
            if not line:
                continue

            try:
                data = json.loads(line)
            except:
                continue

            if "response" in data:
                full += data["response"]

            if data.get("done"):
                break

        if full.strip():
            logging.info("Ollama responded successfully.")
            return full.strip()
        else:
            logging.warning("Ollama returned empty response.")
            return None

    except Exception as e:
        logging.exception("Ollama ERROR:")
        return None


# ------------------------------------------------------------
# OPENROUTER FALLBACK
# ------------------------------------------------------------
def ask_openrouter(prompt, timeout=40):
    if not OPENROUTER_API_KEY:
        return None

    logging.info("Using OpenRouter fallback...")

    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        body = {
            "model": "openrouter/auto",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 512
        }

        r = requests.post(OPENROUTER_URL, headers=headers, json=body, timeout=timeout)
        r.raise_for_status()
        data = r.json()

        msg = data["choices"][0]["message"]["content"]
        logging.info("OpenRouter returned a response.")
        return msg.strip()

    except Exception as e:
        logging.exception("OpenRouter ERROR:")
        return None


# ------------------------------------------------------------
# TEMPLATE LOADER
# ------------------------------------------------------------
def load_template(name):
    return open(f"templates/{name}", "r", encoding="utf-8").read()


TEMPLATES = {
    "day0": load_template("day0_prompt.txt"),
    "day1": load_template("day1_prompt.txt"),
    "day3": load_template("day3_prompt.txt"),
    "day7": load_template("day7_prompt.txt"),
}


# ------------------------------------------------------------
# BUILD PROMPT
# ------------------------------------------------------------
def build_prompt(template, lead):
    return template.format(**lead)


# ------------------------------------------------------------
# SAFE DATE PARSER
# ------------------------------------------------------------
def parse_date(d):
    if not d:
        return None
    try:
        return dtparser.parse(str(d)).date()
    except:
        return None


# ------------------------------------------------------------
# MAIN AUTOMATION LOGIC
# ------------------------------------------------------------
def run_bot():

    logging.info("=== Bot Execution Started ===")

    ws = connect_sheets()
    rows = ws.get_all_records()
    header = ws.row_values(1)
    col = {c: i + 1 for i, c in enumerate(header)}
    today = date.today()

    for i, row in enumerate(rows, start=2):

        lead = {
            "timestamp": row.get("Timestamp", "").strip(),
            "name": row.get("LeadName", "").strip(),
            "email": row.get("Email", "").strip(),
            "company": row.get("Company", "").strip(),
            "product": row.get("Product", "").strip(),
            "source": row.get("Source", "").strip(),
            "notes": row.get("LeadNotes", "").strip(),
        }

        if not lead["email"]:
            continue

        logging.info(f"Processing lead → {lead['email']}")

        sent0 = str(row.get("Day0_sent", "")).lower() in ("true", "1", "yes")
        sent1 = str(row.get("Day1_sent", "")).lower() in ("true", "1", "yes")
        sent3 = str(row.get("Day3_sent", "")).lower() in ("true", "1", "yes")
        sent7 = str(row.get("Day7_sent", "")).lower() in ("true", "1", "yes")

        last_dt = parse_date(row.get("LastUpdated", "")) or today
        days = (today - last_dt).days

        to_send = None
        if not sent0 and days >= 0:
            to_send = "day0"
        elif not sent1 and days >= 1:
            to_send = "day1"
        elif not sent3 and days >= 3:
            to_send = "day3"
        elif not sent7 and days >= 7:
            to_send = "day7"

        if not to_send:
            continue

        logging.info(f"Selected follow-up: {to_send} for {lead['email']}")

        template = TEMPLATES[to_send]
        prompt = build_prompt(template, lead)

        # AI GENERATION
        ai_text = ask_ollama(prompt) or ask_openrouter(prompt)

        if not ai_text:
            logging.error(f"AI failed for → {lead['email']}")
            continue

        logging.info(f"AI generation successful for {lead['email']}")

        html_body = (
            f"<p>Hi {lead['name']},</p>"
            f"<p>{ai_text}</p>"
            f"<p>Best regards,<br>{FROM_NAME}</p>"
        )

        subject = f"{DEFAULT_SUBJECT} — {lead['product']}" if lead["product"] else DEFAULT_SUBJECT

        try:
            send_email(lead["email"], subject, html_body)
            logging.info(f"EMAIL SENT → {lead['email']} ({to_send})")
        except Exception as e:
            logging.exception(f"EMAIL FAILED for → {lead['email']}")
            continue

        flag_col = {
            "day0": "Day0_sent",
            "day1": "Day1_sent",
            "day3": "Day3_sent",
            "day7": "Day7_sent",
        }[to_send]

        ws.update_cell(i, col[flag_col], "TRUE")
        ws.update_cell(i, col["LastEmailBody"], ai_text)
        ws.update_cell(i, col["LastUpdated"], today.isoformat())

        logging.info(f"Google Sheet updated for → {lead['email']} ({to_send})")

        time.sleep(1.2)

    logging.info("=== Bot Execution Finished ===")


# ------------------------------------------------------------
# RUN
# ------------------------------------------------------------
if __name__ == "__main__":
    print("🚀 AI Follow-Up Agent Started...")
    logging.info("Follow-Up Agent started by user.")
    run_bot()
