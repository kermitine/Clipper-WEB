from __future__ import annotations

from flask import Flask, jsonify, render_template, request

from clipperDecryption.decryption import Decryption
from clipperEncryption.encryption import Encryption
from seedGeneration.seedGen import seedGeneration

app = Flask(__name__)


def process_clipper_text(text: str, seed_word: str, mode: str) -> str:
    seed = seedGeneration(seed_word)
    words = [word for word in text.split() if word]
    if not words:
        raise ValueError("Please enter some text to convert.")

    transformed_words = []
    for index, word in enumerate(words, start=1):
        if mode == "decrypt":
            transformed_words.append(Decryption(word, seed, index))
        else:
            transformed_words.append(Encryption(word, seed, index))

    return " ".join(transformed_words)


@app.route("/")
def home():
    return render_template("index.html", embed_mode=False)


@app.route("/embed")
def embed():
    return render_template("index.html", embed_mode=True)


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/api/convert")
def convert():
    payload = request.get_json(silent=True) or {}
    text = (payload.get("text") or "").strip()
    seed_word = (payload.get("seed_word") or "").strip()
    mode = (payload.get("mode") or "encrypt").lower()

    if not seed_word:
        return jsonify({"error": "A seed word is required."}), 400
    if not text:
        return jsonify({"error": "Text to convert is required."}), 400
    if mode not in {"encrypt", "decrypt"}:
        return jsonify({"error": "Mode must be either 'encrypt' or 'decrypt'."}), 400

    try:
        result = process_clipper_text(text, seed_word, mode)
    except Exception as exc:  # pragma: no cover - defensive path
        return jsonify({"error": str(exc)}), 500

    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
