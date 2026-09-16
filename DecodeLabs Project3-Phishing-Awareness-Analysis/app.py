from flask import Flask, render_template, request, jsonify
import re
from urllib.parse import urlparse

app = Flask(__name__)

RULES = [
    ("Urgent or threatening language", "Creates pressure by demanding immediate action.", ["urgent","immediately","act now","action required","final warning","within 24 hours"], 15),
    ("Credential request", "Requests usernames, passwords, login details, or account verification.", ["password","username","login details","login credentials","verify your identity","confirm your account"], 20),
    ("OTP / verification code request", "Requests an OTP, verification code, or security code.", ["otp","verification code","security code","one time password","one-time password"], 20),
    ("Financial information request", "Requests banking, card, payment, or money-transfer information.", ["credit card","debit card","card number","bank account","account number","payment","transfer money","cvv"], 20),
    ("Account suspension threat", "Threatens account closure, suspension, locking, or loss of access.", ["account suspended","account will be closed","account will be locked","lose access","account termination","suspended"], 15),
    ("Unexpected reward or prize", "Uses prizes, rewards, or gifts to attract attention.", ["you won","winner","prize","reward","claim your","congratulations","free gift"], 15),
    ("Suspicious call to action", "Pushes the recipient to click, open, verify, or submit information.", ["click here","click the link","open the link","verify now","update now","confirm now"], 15),
]

EXAMPLES = [
"""URGENT: Your bank account has been suspended.

We detected unusual activity on your account.
You must verify your identity immediately.

Click here to verify:
http://192.168.1.25/verify-account

Please enter your username, password and OTP.
Failure to complete verification within 24 hours will result in account termination.""",
"""Congratulations! You are today's lucky winner.

You have won a free gift worth Rs. 50,000.
Claim your reward immediately:
http://delivery-check.example/claim-prize

Send your account number and verification code to complete the claim.""",
"""Your package could not be delivered.

Action required: update your delivery information within 24 hours.
Click here to confirm your address and payment details:
http://delivery-check.example/confirm"""
]

def urls_in(text):
    return [u.rstrip(".,!?);]}>") for u in re.findall(r'https?://[^\s<>"\']+|www\.[^\s<>"\']+', text, re.I)]

def scan_url(url):
    candidate = url if re.match(r'^[a-z]+://', url, re.I) else 'http://' + url
    p = urlparse(candidate)
    host = p.hostname or ""
    reasons, score = [], 0
    if p.scheme.lower() == "http":
        reasons.append("Uses HTTP instead of HTTPS"); score += 20
    if re.fullmatch(r'\d{1,3}(?:\.\d{1,3}){3}', host):
        reasons.append("Uses an IP address instead of a normal domain"); score += 30
    if "@" in candidate:
        reasons.append("Contains @, which can hide the apparent destination"); score += 25
    if len(url) > 100:
        reasons.append("Unusually long URL"); score += 10
    if len(host.split(".")) >= 5:
        reasons.append("Contains many subdomains"); score += 10
    if host.lower() in {"bit.ly","tinyurl.com","t.co","is.gd","ow.ly"}:
        reasons.append("Uses a URL-shortening service"); score += 20
    if "xn--" in host:
        reasons.append("Contains a punycode hostname"); score += 20
    if any(x in url.lower() for x in ["login","verify","password","secure","account","update","bank"]):
        reasons.append("Contains sensitive-action wording"); score += 10
    score = min(score, 100)
    level = "Critical" if score >= 70 else "High" if score >= 45 else "Suspicious" if score >= 20 else "Low"
    return {"url": url, "domain": host or "Unknown", "score": score, "risk_level": level, "reasons": reasons}

def message_type(text):
    t = text.lower()
    if any(x in t for x in ["bank","banking","credit card","debit card","transaction"]): return "Banking"
    if any(x in t for x in ["delivery","package","parcel","shipment","courier"]): return "Delivery"
    if any(x in t for x in ["prize","winner","reward","congratulations"]): return "Prize / Reward"
    if any(x in t for x in ["otp","verification code","security code","one-time password"]): return "Verification"
    if any(x in t for x in ["password","login","account","verify your identity"]): return "Account Security"
    return "General Message"

def analyze(text):
    t = text.lower()
    flags, score = [], 0
    for name, desc, words, points in RULES:
        if any(w in t for w in words):
            flags.append({"name": name, "description": desc})
            score += points
    scanned_urls = [scan_url(u) for u in urls_in(text)]
    for u in scanned_urls:
        flags.append({
            "name": "Suspicious URL characteristics" if u["score"] >= 20 else "External link detected",
            "description": "The link has structural warning signs." if u["score"] >= 20 else "Verify the destination before opening the link."
        })
        if u["score"] >= 20: score += 15
    score = min(score, 100)
    level = "Critical" if score >= 75 else "High" if score >= 50 else "Suspicious" if score >= 25 else "Low"
    summaries = {
        "Critical": ("Multiple strong phishing indicators were detected.",
                     "Avoid clicking links, replying, or sharing sensitive information.",
                     "Do not interact. Verify the request through an official channel and report it."),
        "High": ("Several suspicious indicators were detected.",
                 "The message contains multiple phishing warning signs.",
                 "Do not click links or provide information until independently verified."),
        "Suspicious": ("Some phishing indicators were detected.",
                       "The message deserves additional verification.",
                       "Check the sender, inspect links, and verify through an official source."),
        "Low": ("Few or no phishing indicators were detected.",
                "This rule-based check found no major phishing patterns, but it cannot guarantee safety.",
                "Continue to verify unexpected requests before sharing sensitive information.")
    }
    summary, explanation, action = summaries[level]
    return {"score":score,"risk_level":level,"summary":summary,"explanation":explanation,
            "action":action,"message_type":message_type(text),"flags":flags,"urls":scanned_urls}

@app.route("/")
def home(): return render_template("page.html", page="dashboard", examples=EXAMPLES, rules=RULES)
@app.route("/<page>")
def pages(page):
    allowed = {"dashboard","analyzer","url-scanner","red-flags","examples","checklist","safety-tips"}
    if page not in allowed: return ("Not Found",404)
    return render_template("page.html", page=page, examples=EXAMPLES, rules=RULES)

@app.post("/api/analyze")
def api_analyze():
    data = request.get_json(silent=True) or {}
    text = str(data.get("text","")).strip()
    if not text: return jsonify(error="Please enter a message."), 400
    return jsonify(analyze(text))

@app.post("/api/scan-url")
def api_scan_url():
    data = request.get_json(silent=True) or {}
    url = str(data.get("url","")).strip()
    if not re.match(r'^(https?://|www\.)', url, re.I):
        return jsonify(error="Enter a URL beginning with http://, https://, or www."), 400
    return jsonify(scan_url(url))

if __name__ == "__main__":
    app.run(debug=True)
