# PhishGuard-AI
An AI-powered phishing detection system that uses Machine Learning and optional LLM integration to identify malicious URLs and suspicious emails. Built with Python, Flask, Scikit-learn, and NLP, featuring real-time scanning, threat analysis, risk classification, and scan history.


# PhishGuard AI 🛡️

### AI-Powered Phishing Detection and Analysis System

PhishGuard AI is a cybersecurity project designed to identify phishing attacks through intelligent URL and email analysis. It combines Machine Learning algorithms, rule-based detection, and optional Large Language Model (LLM) integration to analyze suspicious links and email messages.

The system provides a user-friendly web dashboard where users can scan URLs and email content, identify potential phishing threats, view detection scores, and understand security risks.

### Key Features

- **URL Phishing Detection:** Identifies potentially malicious and suspicious URLs.
- **Email Phishing Detection:** Analyzes email content to detect phishing attempts.
- **Machine Learning:** Uses Random Forest and Logistic Regression algorithms.
- **AI Integration:** Optional OpenAI or Anthropic LLM integration for contextual analysis.
- **Risk Classification:** Classifies results as Phishing, Suspicious, or Legitimate.
- **Red Flag Detection:** Identifies suspicious keywords, urgency, and credential requests.
- **Web Dashboard:** Interactive interface built using Flask and HTML.
- **REST API:** Provides endpoints for URL and email scanning.
- **Scan History:** Stores previous scan results using SQLite.

### Technology Stack

- **Programming Language:** Python
- **Backend:** Flask
- **Frontend:** HTML, CSS, JavaScript
- **Machine Learning:** Scikit-learn
- **NLP:** TF-IDF
- **Algorithms:** Random Forest, Logistic Regression
- **Database:** SQLite
- **AI Integration:** OpenAI / Anthropic API (optional)
- **Model Storage:** Joblib

### Project Objective

The main objective of PhishGuard AI is to improve phishing awareness and support early identification of suspicious URLs and email messages through automated cybersecurity analysis.

### Disclaimer

This project is developed for educational and cybersecurity research purposes. Detection results are predictions and should not be treated as a guarantee that a URL or email is safe.
