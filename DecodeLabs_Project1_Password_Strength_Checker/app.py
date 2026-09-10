from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

COMMON_PASSWORDS = {
    "password", "password123", "123456", "12345678", "qwerty",
    "qwerty123", "admin", "letmein", "welcome", "iloveyou", "abc123"
}

def analyze_password(password):
    length = len(password)
    has_uppercase = any(c.isupper() for c in password)
    has_lowercase = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(not c.isalnum() for c in password)

    checks = {
        "length": length >= 8,
        "uppercase": has_uppercase,
        "lowercase": has_lowercase,
        "number": has_digit,
        "symbol": has_symbol
    }

    score = sum(checks.values())
    common = password.lower() in COMMON_PASSWORDS

    if length < 8 or common:
        strength = "Weak"
    elif score == 5 and length >= 12:
        strength = "Strong"
    elif score >= 3:
        strength = "Medium"
    else:
        strength = "Weak"

    suggestions = []
    if length < 8: suggestions.append("Use at least 8 characters.")
    elif length < 12: suggestions.append("Aim for 12+ characters for better protection.")
    if not has_uppercase: suggestions.append("Add an uppercase letter.")
    if not has_lowercase: suggestions.append("Add a lowercase letter.")
    if not has_digit: suggestions.append("Add a number.")
    if not has_symbol: suggestions.append("Add a special symbol.")
    if common: suggestions.append("Avoid common or easily guessed passwords.")
    if not suggestions: suggestions.append("Excellent — all project checks passed.")

    return {"strength": strength, "score": score, "max_score": 5,
            "checks": checks, "common": common, "suggestions": suggestions}

@app.get("/")
def home():
    return render_template("index.html")

@app.post("/analyze")
def analyze():
    data = request.get_json(silent=True) or {}
    password = data.get("password", "")
    if not isinstance(password, str):
        return jsonify({"error": "Invalid input"}), 400
    return jsonify(analyze_password(password))

if __name__ == "__main__":
    app.run(debug=True)
