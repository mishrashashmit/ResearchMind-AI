# ResearchMind AI - Multi-Agent Research Assistant

> A production-quality Python application that searches for research papers, generates intelligent summaries, extracts key topics, identifies emerging research trends, and exports professional PDF reports.

## 🎯 Overview

**ResearchMind AI** is an intelligent research analysis system powered by Google's Gemini API. It automates the research paper discovery and analysis workflow through a coordinated multi-agent architecture:

1. **Search Agent** - Discovers research papers on a given topic
2. **Summary Agent** - Generates detailed summaries of papers
3. **Topic Agent** - Extracts key research topics and themes
4. **Trend Agent** - Identifies emerging research trends
5. **PDF Generator** - Exports professional analysis reports

The system provides both a **web interface** (Streamlit) and **command-line interface** (CLI) for flexible usage.

## ✨ Features

* 🔍 Research paper discovery
* 📝 AI-generated paper summaries
* 🏷️ Topic extraction from papers
* 📈 Emerging trend identification
* 📄 Professional PDF report generation
* 🕘 Search history tracking
* 🎨 Modern Streamlit dashboard

---

## 🏗️ Architecture

```text
User Query
     │
     ▼
Search Agent
     │
     ▼
Summary Agent
     │
     ▼
Topic Agent
     │
     ▼
Trend Agent
     │
     ▼
PDF Generator
```

---

## 🛠️ Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Language** | Python | 3.11+ |
| **AI API** | Google Gemini API | gemini-1.5-flash |
| **Web UI** | Streamlit | 1.28.0+ |
| **PDF Generation** | ReportLab | 4.0.0+ |
| **API Client** | google-generativeai | 0.6.0 |
| **Environment** | python-dotenv | 1.0.0+ |
| **HTTP** | requests | 2.31.0+ |
| **Image Processing** | Pillow | 10.0.0+ |

---

## 📂 Project Structure

```
ResearchMind-ai/
│
├── config.py                 # Configuration, API setup, logging
├── main.py                   # ResearchAnalyzer orchestrator & CLI
├── requirements.txt          # Project dependencies
├── .env                      # Environment variables (API keys)
│
├── agents/                   # Research agents
│   ├── search_agent.py       # Paper discovery via Gemini API
│   ├── summary_agent.py      # Paper summarization
│   ├── topic_agent.py        # Topic extraction
│   └── trend_agent.py        # Trend identification
│
├── tools/                    # Utility functions
│   ├── paper_counter.py      # Paper statistics & filtering
│   └── pdf_generator.py      # PDF report generation (ReportLab)
│
├── app/                      # Streamlit web interface
│   └── streamlit_app.py      # Interactive UI
│
├── outputs/                  # Generated files
│   ├── reports/              # PDF reports (auto-created)
│   └── logs/                 # Application logs (auto-created)
│
└── README.md                 # This file
```

## 📊 Data Flow

```
User Input (Topic)
        ↓
[Search Agent] → Finds papers on topic
        ↓
     Papers List
        ↓
[Summary Agent] → Creates detailed summaries
        ↓
    Summarized Papers
        ↓
[Topic Agent] → Extracts key topics
        ↓
    Topics List
        ↓
[Trend Agent] → Identifies trends
        ↓
    Trends List
        ↓
[Paper Counter] → Calculates statistics
        ↓
    Statistics
        ↓
[PDF Generator] → Creates professional report
        ↓
    PDF File (outputs/reports/)
```

## 🔄 API Response Handling

ResearchMind AI is built to handle common API and data issues gracefully.

| Scenario | Behavior |
|----------|----------|
| No papers found | Shows a user-friendly message and stops analysis safely |
| Topic extraction fails | Continues with summaries and report generation |
| Only one paper available | Skips trend analysis and informs the user |
| Invalid/Incomplete paper data | Skips the affected paper and continues |
| Empty or malformed API response | Logs the issue and handles it safely |
| API quota exceeded | Displays an error message without crashing |
| PDF generation failure | Preserves analysis results and reports the error |

### Key Features
- Graceful error handling
- Batch API processing for efficiency
- User-friendly warnings
- Comprehensive logging

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/mishrashashmit/ResearchMind-ai
cd ResearchMind-ai
```

Create virtual environment:

```bash
python -m venv venv
```

Activate environment:

```bash
# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

---

## 🚀 How to Run ResearchMind AI

```text
1-Run via Web App(Streamlit)
```
```bash
streamlit run app/streamlit_app.py
```

Open:

```text
http://localhost:8501
```

---
```text
1-Run via CLI
```
```bash
python main.py
```
```What you will see -
============================================================
ResearchMind AI - Multi-Agent Research Assistant
============================================================
researchmind - INFO - ResearchAnalyzer initialized

🔬 ResearchMind CLI
------------------------------------------------------------
1. Analyze research topic
2. Exit
------------------------------------------------------------
Select option (1-2):

```
## 📸 Demo

Add screenshots here:

```
assets/homepage.png
assets/results.png
assets/pdf_report.png
```

---

## 🚀 Future Improvements

- Integrate real research databases (ArXiv, Semantic Scholar).
- Add caching to reduce API usage and improve response time.
- Support multiple LLM providers for better reliability.
- Improve trend analysis with publication timeline insights.
- Enable cloud deployment with user authentication.

---

## 👨‍💻 Contributors

Developed by AI & Software Enthusiasts:

* Shashmit Mishra    
* Sanskar Pandey

For any collaboration, contact:
Mail id : mishrashashmit09@gmail.com
LinkedIn: https://www.linkedin.com/in/shashmit-mishra-9675ab273/

---

## ⭐ Support

If you found this project useful, consider giving it a star.