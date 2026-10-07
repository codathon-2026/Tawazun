# 🪞 Tawazun — توازن

**AI media wellbeing for Libya**

Tawazun helps people assess online content, understand its emotional impact, and choose how to respond — without political judgment, diagnosis, or bias.

> **"Lest you're immune… but you can become so."**

---

## 📌 The Problem

In Libya, online content creates two challenges at once:

- People must judge whether a post is credible.
- They must manage how its language makes them feel.

Misinformation, inflammatory rhetoric, and hate speech mix with urgency and emotional pressure. In June 2026, the UN in Libya raised concern about misinformation, disinformation, and inflammatory rhetoric on social media, including content targeting individuals and groups.

**88.5%** of Libya's population used the internet at the end of 2025 — making this a highly relevant setting.

---

## 💡 The Solution

Tawazun is an AI media wellbeing platform for Libya. It helps users:

1. **Read the post** — spot loaded language, unsupported claims, urgency, or targeting.
2. **Notice the impact** — name the feeling the content brought up, without judgment.
3. **Choose a response** — pause, check a source, try a grounding prompt, or disengage.

AI supports reflection. It does not decide what people should believe.

---

## ⚙️ Features

### Understand Content
| # | Feature | Description |
|---|---|---|
| 01 | **Misinformation Detector** | Explains claim and persuasion signals with uncertainty. |
| 02 | **Source Checker** | Surfaces source cues and points to trusted references. |
| 03 | **Post Simulator** | Lets users practice spotting misleading techniques. |

### Notice and Respond
| # | Feature | Description |
|---|---|---|
| 04 | **Psychological Impact Analyzer** | Connects content with user-reported feelings. |
| 05 | **Mood & Media Tracker** | Shows opt-in patterns and suggests a media break. |
| 06 | **Hate-Speech Response Coach** | Offers ways to respond calmly or disengage. |

### Libyan Arabic Support
| # | Feature | Description |
|---|---|---|
| 07 | **Story Companion — "Al-Hakeem"** | Uses reviewed Libyan Arabic stories for reflection. |

Local reviewers guide language, examples, and resources across all seven features.

---

## 🧠 How It Works

~~~
INPUT
Posts, links, or practice examples
        │
        ▼
AI ANALYSIS
Claim cues, source signals, emotional language, hate speech
        │
        ▼
USER CONTEXT
Self-reported feeling + optional mood history
        │
        ▼
SUPPORT
Source guidance, calming prompts, practice, stories, response coaching
        │
        ▼
DESIGNED OUTCOME
Users understand what a post is doing, how it affects them,
and which next step they want to take.
~~~

---

## 🛠️ Tech Stack (MVP — 36-hour build)

| Layer | Tools |
|---|---|
| **AI** | Gemini API / OpenAI GPT-4o, prompt engineering (Arabic + Libyan dialect), JSON outputs, no fine-tuning |
| **Frontend** | Streamlit, RTL Arabic, mobile-first layout |
| **Backend** | Python (single `app.py`), 7 modular functions, JSON files, no database |
| **Data** | `stories.json`, `examples.json`, `sources.json`, `prompts.json` |
| **Deploy** | Streamlit Cloud, GitHub, backup demo video |

> **No training. No database. No backend. Just prompts + APIs + 36 hours.**

---

## 🚀 Run Locally

### Prerequisites
- Python 3.10+
- A Gemini or OpenAI API key

### Setup

~~~
# Clone the repo
git clone https://github.com/your-username/tawazun.git
cd tawazun

# Install dependencies
pip install -r requirements.txt

# Set your API key
export GEMINI_API_KEY="your-key-here"
# or
export OPENAI_API_KEY="your-key-here"

# Run the app
streamlit run app.py
~~~

Then open `http://localhost:8501` in your browser.

---

## 📁 Project Structure

~~~
tawazun/
├── app.py                  # Main Streamlit app
├── functions/
│   ├── analyze_post.py     # Misinformation detector
│   ├── check_source.py     # Source checker
│   ├── simulate_post.py    # Post simulator
│   ├── analyze_impact.py   # Psychological impact analyzer
│   ├── track_mood.py       # Mood & media tracker
│   ├── coach_response.py   # Hate-speech response coach
│   └── tell_story.py       # Al-Hakeem companion
├── data/
│   ├── stories.json        # Reviewed Libyan stories
│   ├── examples.json       # Labeled posts for practice
│   ├── sources.json        # Trusted references
│   └── prompts.json        # Prompt templates
├── requirements.txt
└── README.md
~~~

---

## 🛡️ AI's Role & Safety Boundaries

### AI can:
- Explain emotional or persuasive techniques in plain language.
- Reflect the feeling a user chooses to share.
- Suggest a reviewed activity or source-checking step.

### The product should:
- Show uncertainty and explain why a signal was flagged.
- Avoid political judgments, diagnoses, or certainty scores.
- Minimize data collection and let users skip or delete.

> **AI supports reflection. It does not decide what people should believe.**

---

## 🎯 Roadmap

| Phase | Timeline | Goal |
|---|---|---|
| 1 | Month 1–2 | MVP on WhatsApp / Telegram |
| 2 | Month 3–4 | Pilot with university + school |
| 3 | Month 5–6 | Mobile app launch + media campaign |
| 4 | Month 7–9 | Institutional partnerships |
| 5 | Month 10–12 | Expand to Arab region |

---

## 📚 Sources & Evidence Notes

- **Digital access:** DataReportal, *Digital 2026: Libya* (published Nov 2025; underlying internet figures late 2025). [Link](https://datareportal.com/reports/digital-2026-libya)
- **Misinformation context:** United Nations in Libya, statement on misinformation and inflammatory rhetoric, 1 June 2026. [Link](https://libya.un.org/en/316507-un-libya-expresses-concern-over-spread-misinformation-and-inflammatory-rhetoric)
- **Mental-health context:** WHO EMRO, *Mental health and psychosocial support* (2024 report). The 22.1% figure refers to conflict-affected populations, not a Libya-specific prevalence survey. [Link](https://applications.emro.who.int/docs/9789292741716-eng.pdf)
- **National data limitation:** WHO Libya country profile: public mental-health research is limited; mental-health data are not routinely collected in national health information systems. [Link](https://www.who.int/about/accountability/results/who-results-report-2024-2025/region-EMRO/2024/libya)

---

## 👥 Team

- **Suliman Hashem**
- **Buthina Urayet**
- **Abdulhafiz Al-Sallai**

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Libyan community reviewers and mental-health experts.
- Open-source Arabic NLP community.
- United Nations in Libya, WHO EMRO, and DataReportal for public data.

---

> **Tawazun connects content understanding with emotional wellbeing, in a form designed for Libya.**

