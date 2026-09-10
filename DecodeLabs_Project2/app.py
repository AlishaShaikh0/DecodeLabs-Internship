from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


def caesar_encrypt(text, shift):
    """
    Encrypt text using the Caesar cipher.
    Letters are shifted while numbers, spaces and symbols remain unchanged.
    """
    result = ""

    for char in text:
        if char.isalpha():
            base = ord("A") if char.isupper() else ord("a")
            shifted = chr((ord(char) - base + shift) % 26 + base)
            result += shifted
        else:
            result += char

    return result


def caesar_decrypt(text, shift):
    """
    Decrypt text by reversing the Caesar cipher shift.
    """
    return caesar_encrypt(text, -shift)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/encrypt", methods=["POST"])
def encrypt():
    data = request.get_json()

    text = data.get("text", "").strip()

    try:
        shift = int(data.get("shift", 3))
    except (TypeError, ValueError):
        return jsonify({"error": "Shift key must be a number."}), 400

    if not text:
        return jsonify({"error": "Please enter some text to encrypt."}), 400

    encrypted = caesar_encrypt(text, shift)

    return jsonify({
        "encrypted": encrypted,
        "shift": shift
    })


@app.route("/decrypt", methods=["POST"])
def decrypt():
    data = request.get_json()

    text = data.get("text", "").strip()

    try:
        shift = int(data.get("shift", 3))
    except (TypeError, ValueError):
        return jsonify({"error": "Shift key must be a number."}), 400

    if not text:
        return jsonify({"error": "Please enter some text to decrypt."}), 400

    decrypted = caesar_decrypt(text, shift)

    return jsonify({
        "decrypted": decrypted,
        "shift": shift
    })


if __name__ == "__main__":
    app.run(debug=True)