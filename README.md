# PhishGuard AI — AI-Integrated Phishing Detection System

A hybrid phishing detection system that combines **Machine Learning** (fast, explainable scoring) with an optional **Large Language Model** (contextual second opinion and plain-English explanation). It scans both **URLs** and **email text**, through a web dashboard, a REST API or the command line.

## Architecture

```
            ┌──────────────┐
 URL ──────►│ URL features │──► Random Forest ──────┐
            │ (24 lexical) │                        │
            └──────────────┘                        ▼
                                             ┌─────────────┐     ┌───────────────┐
 Email ───► clean text ─► TF-IDF ─► LogReg ─►│ ML score    │────►│ Hybrid fusion │──► Verdict
   │                                         │ + red flags │     │ 0.6·ML+0.4·LLM│   phishing /
   └──► links extracted ─► URL model ───────►└─────────────┘     └───────▲───────┘   suspicious /
                                                   │                     │           legitimate
                                                   └──► LLM (optional) ──┘
                                                        JSON verdict + reasons + advice
```

| Layer | Technique | Role |
|---|---|---|
| URL model | Random Forest on 24 lexical features (IP host, `@`, TLD, brand impersonation, entropy, shorteners, punycode…) | Detects malicious links |
| Email model | TF-IDF (1–2 grams) + Logistic Regression | Detects phishing language |
| Rule engine | Urgency, credential requests, money bait, generic greetings | Human-readable red flags |
| AI layer | Claude or OpenAI LLM via API, structured JSON output | Second opinion and explanation |
| Fusion | Weighted score; thresholds 0.7 / 0.4 | Final verdict |
| Logging | SQLite scan history | Audit trail |

## Project structure

```
phishing-detector/
├── app.py                  Flask web app + REST API
├── requirements.txt
├── data/
│   ├── generate_dataset.py Synthetic starter dataset
│   ├── urls.csv            url,label
│   └── emails.csv          text,label
├── src/
│   ├── features.py         URL + email feature extraction, red flags
│   ├── train.py            Trains both models, writes metrics.json
│   ├── llm_analyzer.py     Optional LLM integration (standard library only)
│   └── detector.py         Hybrid detector + CLI
├── models/                 Trained .joblib models + metrics.json
├── templates/index.html    Dashboard UI
└── tests/test_detector.py  Unit tests (pytest)
```

## Setup and run

```bash
pip install -r requirements.txt
python data/generate_dataset.py     # creates data/urls.csv and data/emails.csv
python src/train.py                 # trains models -> models/
python app.py                       # open http://127.0.0.1:5000
```

Turn on the AI layer (optional) by setting one key before starting the app:

```bash
# Linux / macOS
export ANTHROPIC_API_KEY=your_key        # or: export OPENAI_API_KEY=your_key
# Windows PowerShell
$env:ANTHROPIC_API_KEY="your_key"
```

Without a key, the system still works fully using ML + rule-based explanations.

### Command line

```bash
python src/detector.py --url "http://192.168.1.4/sbi/login/verify" --no-llm
python src/detector.py --email @suspicious_mail.txt
```

### REST API

```bash
curl -X POST http://127.0.0.1:5000/api/scan/url   -H "Content-Type: application/json" -d '{"url":"http://paypal-verify.xyz/login"}'
curl -X POST http://127.0.0.1:5000/api/scan/email -H "Content-Type: application/json" -d '{"text":"Dear customer, verify your account..."}'
curl http://127.0.0.1:5000/api/metrics
curl http://127.0.0.1:5000/api/history
```

### Tests

```bash
python -m pytest tests -q
```

## Using real datasets (important for your report)

The bundled data is **synthetic** so the project runs immediately. Models score ~100% on it because the
synthetic patterns are easy to separate — **these numbers are not meaningful for a report**. Before
presenting results, replace the CSVs with real data (keep the same column names) and retrain:

- **URLs:** PhishTank, OpenPhish, Kaggle "Phishing Site URLs" / "Malicious URLs dataset"; legitimate URLs from the Tranco top-sites list
- **Emails:** Nazario phishing corpus, Kaggle "Phishing Email Detection"; legitimate mail from the Enron corpus

Then run `python src/train.py` again; the dashboard picks up the new `metrics.json` automatically.

## Possible extensions

- WHOIS domain age, DNS and SSL certificate features (needs network lookups)
- Fine-tuned transformer (DistilBERT) for email text
- Browser extension that calls `/api/scan/url` before a page loads
- Screenshot-based visual brand-impersonation detection
- SHAP values for per-feature explanations
