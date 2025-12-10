🚀 AI Lead Follow-Up Agent
Automated Email Follow-Up System using Python, Google Sheets, Gmail API, and Local AI (Ollama) and openrouter

This project is a fully automated AI-powered lead follow-up system built with Python, designed for businesses that want consistent, personalized follow-up without using Zapier, Make.com, or paid automation tools.

It includes:

🧠 AI-generated emails (Day 0, Day 1, Day 3, Day 7)

📊 A beautiful dashboard UI (Tailwind + Vercel demo)

📩 Gmail API email sending

🗂 Google Sheets CRM

🤖 Local AI support using Ollama (Llama3/Mistral)

🌐 Optional OpenRouter support

⚙ Fully automated via cron/Task Scheduler

📈 Lead progress tracking + analytics



Automated Emails

Google Sheet CRM

⭐ Features
✔ 1. Automated follow-ups

The system sends emails automatically based on the lead's timeline:

Stage	Description
Day0	Intro email sent immediately
Day1	Short follow-up referencing previous email
Day3	Value-based follow-up with CTA
Day7	Final follow-up with soft close
✔ 2. Google Sheets as a CRM

The system reads & updates a Google Sheet with fields:

Timestamp | LeadName | Email | Company | Product | Source | LeadNotes |
Day0_sent | Day1_sent | Day3_sent | Day7_sent | LastUpdated | LastEmailBody


Each row represents a lead.

✔ 3. AI Email Generation

Uses:

🧠 Ollama (local models)
– Llama3
– Llama3.1
– Mistral
– Any local model

or

🌍 OpenRouter (optional cloud backup)

✔ 4. Clean, Modern Dashboard

Built using Flask + TailwindCSS, including:

Real-time lead stats

Follow-up progress bars

Color-coded statuses

Open sheet link

Logs viewer

Live Demo (Frontend Only) →
👉 https://followupagentdemo-mp506xmit-hemantdhaker00-gmailcoms-projects.vercel.app/

✔ 5. Secure & No Paid Tools Required

This system uses:

✔ Free Google APIs

✔ Local AI (Ollama)

✔ Free Gmail SMTP

✔ Free deployment options

🏗️ Architecture Overview
+------------------+
| Google Sheet CRM |
+------------------+
          |
          v
+---------------------+       +----------------------+
| Python Automation   | --->  | Gmail API (SMTP)     |
| main.py             |       +----------------------+
| - Reads leads       |
| - AI generation     |       +----------------------+
| - Send emails       | --->  | Ollama (Local LLM)   |
| - Update sheet      |       +----------------------+
+---------------------+
          |
          v
+---------------------+
| Dashboard (Flask)   |
| Tailwind UI         |
+---------------------+

⚙ Installation & Setup
1. Clone the repo
git clone https://github.com/HemantDhaker12/AI-Lead-FollowUp-Agent.git
cd AI-Lead-FollowUp-Agent

2. Create virtual environment
python -m venv venv
venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Setup .env

Create a file named .env:

SPREADSHEET_ID=your_sheet_id
SHEET_NAME=Sheet1

GMAIL_FROM=your_email@gmail.com
GMAIL_APP_PASSWORD=xxxx_app_password

FROM_NAME=Your Name
DEFAULT_SUBJECT=Quick question about your interest

OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2:1b

OPENROUTER_API_KEY=

5. Add Google Service Account

Place your downloaded file at:

credentials/google-service-account.json


Share your sheet with the email inside that JSON.

6. Run backend automation
python main.py

7. Run local dashboard
python app/dashboard.py


Open:
👉 http://localhost:5000/

📡 Deployment



📁 Repository Structure
/
├── app/
│   ├── dashboard.py
│   └── templates/
│       ├── index.html
│       ├── leads.html
│       ├── logs.html
│       └── status.html
├── templates/
│   ├── day0_prompt.txt
│   ├── day1_prompt.txt
│   ├── day3_prompt.txt
│   └── day7_prompt.txt
├── main.py
├── config.py
├── requirements.txt
├── demo-ui/   ← Vercel frontend
│   ├── index.html
│   └── demo.html
└── credentials/
    └── google-service-account.json (ignored)

🏆 Why This Project is Valuable

✔ Real client use-case
✔ AI + Automation + Sheets + APIs
✔ Production-level patterns
✔ Resume-ready
✔ Freelancer-ready
✔ High demand in marketing & CRM automations

📬 Contact

If you want to collaborate or need enhancements:

📧 Email: hemantdhaker00@gmail.com
🔗 LinkedIn: https://www.linkedin.com/in/hemant-dhaker-a95044292/