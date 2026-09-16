# PhishGuard — Phishing Awareness & Message Analyzer

A rule-based cybersecurity awareness tool developed as **Project 3 of the DecodeLabs Cyber Security Internship Program**.

PhishGuard helps users analyze suspicious emails, SMS messages, and other communications by identifying common phishing indicators such as urgency, credential requests, OTP requests, financial information requests, suspicious links, and account-suspension threats.

> **Educational Project:** PhishGuard is designed for cybersecurity learning and awareness. It does not guarantee that a message or URL is safe and should not be treated as a replacement for professional security tools.

---

## Project Objective

The objective of this project is to analyze sample messages and identify potential phishing attempts by:

- Detecting suspicious keywords and phrases
- Identifying potentially risky URLs
- Highlighting common phishing red flags
- Explaining why a message may be unsafe
- Assigning a risk score and severity level
- Providing security recommendations
- Promoting safe cybersecurity practices

The project demonstrates practical skills in **threat analysis, phishing awareness, and security thinking**.

---

## Features

### Message Analyzer

Analyze an email, SMS, or social media message for common phishing indicators.
The analyzer provides:

- Risk score from **0–100**
- Risk severity level
- Message type classification
- Number of detected red flags
- Explanation of each detected warning sign
- Recommended security action

### Suspicious URL Scanner

Inspect a URL without actually opening or visiting it.

The scanner checks for characteristics such as:

- HTTP instead of HTTPS
- IP addresses used instead of domain names
- Suspicious URL structure
- Excessive subdomains
- URL shorteners
- Punycode hostnames
- Sensitive-action keywords such as `login`, `verify`, and `account`
- Unusually long URLs

> PhishGuard analyzes the URL as text and does **not visit submitted URLs**.

### Phishing Red Flags

A dedicated awareness section explaining common phishing indicators, including:

- Urgent or threatening language
- Credential requests
- OTP or verification-code requests
- Financial information requests
- Account suspension threats
- Unexpected prizes or rewards
- Suspicious calls to action

### Phishing Examples

Includes fictional phishing scenarios that users can analyze to practice identifying suspicious patterns.

### Security Checklist

An interactive checklist helps users verify a suspicious message before taking action.

Users can check:

1. Sender
2. Request
3. Urgency
4. Link
5. Independent verification
6. Reporting

### Security Awareness Tips

Provides practical guidance for reducing phishing risk, including:

- Slowing down when a message creates urgency
- Never sharing OTPs unexpectedly
- Inspecting links before opening them
- Verifying requests through official channels
- Being cautious of account threats
- Reporting suspicious messages

---

## Risk Classification

PhishGuard uses a rule-based scoring system:

| Score | Risk Level |
|-------|------------|
| 0–24 | 🟢 Low |
| 25–49 | 🟡 Suspicious |
| 50–74 | 🟠 High |
| 75–100 | 🔴 Critical |

The score is based on detected phishing indicators and suspicious URL characteristics.

---

## How It Works

PhishGuard follows a simple defensive workflow:

```text
Suspicious Message
        │
        ▼
Extract Message Content
        │
        ▼
Check Phishing Indicators
        │
        ├── Urgency
        ├── Credential Requests
        ├── OTP Requests
        ├── Financial Requests
        ├── Threats
        └── Suspicious Links
        │
        ▼
Analyze URLs
        │
        ▼
Calculate Risk Score
        │
        ▼
Assign Risk Level
        │
        ▼
Display Red Flags
        │
        ▼
Provide Recommended Action

## Technologies Used
Python
Flask
HTML5
CSS3
JavaScript
Regular Expressions
URL Parsing
Rule-Based Threat Detection

## Security & Privacy Notes

PhishGuard is designed as a defensive cybersecurity awareness project.

The application:

Does not send submitted messages to an external AI service
Does not visit submitted URLs
Performs local rule-based analysis
Uses fictional phishing examples for demonstrations

Users should still verify suspicious communications through trusted and official channels.

## Security & Privacy Notes

PhishGuard is designed as a defensive cybersecurity awareness project.

The application:

Does not send submitted messages to an external AI service
Does not visit submitted URLs
Performs local rule-based analysis
Uses fictional phishing examples for demonstrations

Users should still verify suspicious communications through trusted and official channels.

## Limitations

PhishGuard uses predefined rules and keyword-based detection.

Therefore:

It may produce false positives
It may miss sophisticated phishing attempts
A low score does not guarantee that a message is safe
URL structure alone cannot determine whether a website is malicious
It is not intended to replace enterprise phishing-detection or threat-intelligence platforms

## Internship Project

Program: DecodeLabs Cyber Security Internship
Project: Project 3 — Phishing Awareness Analysis
Focus: Threat Analysis & Cybersecurity Awareness

This project demonstrates practical application of cybersecurity concepts through a web-based defensive awareness tool.

## Author:

Alisha Shaikh
Bachelor's Student — Computer Networks & Security