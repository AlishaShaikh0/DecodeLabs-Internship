# CyberGuard — Password Strength Analyzer
Decode Labs | Cyber Security Internship | Project 1

A professional web interface for the required Password Strength Checker.

## Checks
- Minimum 8 characters
- Uppercase
- Lowercase
- Number
- Special symbol
- Basic common-password detection

## Run on Windows
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
Then open **http://127.0.0.1:5000** in your browser.

## Important
Use test passwords only. Never enter a real personal password.
Passwords are analyzed in memory and are not intentionally stored or logged.
The common-password list is a small educational demo, not a production breach database.
