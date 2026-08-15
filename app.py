from __future__ import annotations

from flask import Flask, jsonify, render_template, request

from vars.ifArray import (
    character_window_index,
    character_window_index_str,
    character_window_inverse_index,
    character_window_inverse_index_int,
    nums,
    special_characters_list,
)
from vars.seedGenVars import (
    seed_generation_index,
    seed_generation_index_int,
    seed_generation_number_index,
)

app = Flask(__name__)


def process_clipper_text(text: str, seed_word: str, mode: str) -> str:
    result, _trace = process_clipper_text_with_trace(text, seed_word, mode)
    return result


def process_clipper_text_with_trace(text: str, seed_word: str, mode: str) -> tuple[str, list[str]]:
    trace = [
        "> clipper console online",
        f"> mode: {mode}",
    ]
    seed = generate_seed_with_trace(seed_word, trace)
    words = [word for word in text.split() if word]
    if not words:
        raise ValueError("Please enter some text to convert.")

    trace.append(f"> input split into {len(words)} word(s): {' | '.join(words)}")

    transformed_words = []
    for index, word in enumerate(words, start=1):
        if mode == "decrypt":
            transformed_words.append(decrypt_word_with_trace(word, seed, index, trace))
        else:
            transformed_words.append(encrypt_word_with_trace(word, seed, index, trace))

    result = " ".join(transformed_words)
    trace.append(f"> final output: {result}")
    trace.append("> process complete")
    return result, trace


def generate_seed_with_trace(seed_word: str, trace: list[str]) -> list[str]:
    seed: list[str] = []
    num_dict = 1
    pop_list: list[int] = []

    trace.append("[seed] starting seed generation")
    trace.append(f"[seed] raw input: {seed_word}")

    seed_word_list = [character.upper() for character in seed_word]
    trace.append(f"[seed] uppercase chars: {format_character_list(seed_word_list)}")

    for index, character in enumerate(seed_word_list):
        if character in special_characters_list or character == " " or character in nums:
            pop_list.append(index)

    if pop_list:
        removed = ", ".join(f"{seed_word_list[index]}@{index}" for index in pop_list)
        trace.append(f"[seed] purging numbers/special chars: {removed}")

    pop_list.sort(reverse=True)
    for index in pop_list:
        seed_word_list.pop(index)

    if not seed_word_list:
        raise ValueError("Seed word must include at least one letter.")

    invalid_chars = [character for character in seed_word_list if character not in seed_generation_index]
    if invalid_chars:
        invalid_display = ", ".join(invalid_chars)
        raise ValueError(f"Seed word contains unsupported character(s): {invalid_display}")

    scramble_times = seed_generation_index_int[seed_word_list[-1]]
    trace.append(
        f"[seed] last char {seed_word_list[-1]} requests {scramble_times} scramble rotation(s)"
    )

    for scramble_index in range(scramble_times):
        seed_word_list = seed_word_list[-1:] + seed_word_list[:-1]
        trace.append(
            f"[seed] scramble {scramble_index + 1:02d}: {format_character_list(seed_word_list)}"
        )

    if len(seed_word_list) > 26:
        trace.append("[seed] slicing seed word to 26 chars")
        seed_word_list = seed_word_list[:26]

    before_dedupe = seed_word_list[:]
    seed_word_list = list(dict.fromkeys(seed_word_list))
    if seed_word_list != before_dedupe:
        trace.append(f"[seed] after duplicate purge: {format_character_list(seed_word_list)}")
    else:
        trace.append("[seed] duplicate purge: no duplicates found")

    for character in seed_word_list:
        seed_value = seed_generation_index[character]
        seed.append(seed_value)
        trace.append(f"[seed] {character} -> {seed_value}")

    trace.append("[seed] filling missing alphabet slots")
    while len(seed) < 26:
        if num_dict > 26:
            num_dict = 1

        next_value = seed_generation_number_index[num_dict]
        if next_value not in seed:
            seed.append(next_value)
            trace.append(f"[seed] filler slot {len(seed):02d}: {next_value}")
            num_dict += 1

        num_dict += 1

    trace.append(f"[seed] generated 52-digit seed: {''.join(seed)}")
    return seed


def encrypt_word_with_trace(word: str, seed: list[str], word_count: int, trace: list[str]) -> str:
    word_list = [character.upper() for character in word]
    trace.append(f"[word {word_count}] encrypt input: {word}")
    trace.append(f"[word {word_count}] uppercase chars: {format_character_list(word_list)}")

    if word_contains_number(word_list):
        unchanged_word = "".join(word_list)
        trace.append(f"[word {word_count}] number found; returning unchanged: {unchanged_word}")
        return unchanged_word

    working_seed = rotate_seed_for_word(seed, word_count, trace)
    pop_list = [
        index
        for index, character in enumerate(word_list)
        if character in special_characters_list
    ]

    if pop_list:
        removed = ", ".join(f"{word_list[index]}@{index}" for index in pop_list)
        trace.append(f"[word {word_count}] removing punctuation/special chars: {removed}")

    pop_list.sort(reverse=True)
    for index in pop_list:
        word_list.pop(index)

    encrypted_list: list[str] = []
    for character in word_list:
        if character == "Z":
            seed_index = 0
            seed_value = working_seed[seed_index]
            trace_prefix = "Z wraps to seed[0]"
        else:
            if character not in character_window_index:
                raise ValueError(f"Unsupported character in input: {character}")

            seed_index = character_window_index[character]
            seed_value = working_seed[seed_index]
            trace_prefix = f"{character} uses alphabet index {seed_index}"

        encrypted_character = character_window_inverse_index[seed_value]
        encrypted_list.append(encrypted_character)
        trace.append(
            f"[word {word_count}] {trace_prefix} -> {seed_value} -> {encrypted_character}"
        )

    encrypted_word = "".join(encrypted_list)
    trace.append(f"[word {word_count}] encrypted word: {encrypted_word}")
    return encrypted_word


def decrypt_word_with_trace(word: str, seed: list[str], word_count: int, trace: list[str]) -> str:
    word_list = [character.upper() for character in word]
    trace.append(f"[word {word_count}] decrypt input: {word}")
    trace.append(f"[word {word_count}] uppercase chars: {format_character_list(word_list)}")

    if word_contains_number(word_list):
        unchanged_word = "".join(word_list)
        trace.append(f"[word {word_count}] number found; returning unchanged: {unchanged_word}")
        return unchanged_word

    working_seed = rotate_seed_for_word(seed, word_count, trace)
    decrypted_word_list: list[str] = []

    for character in word_list:
        if character not in character_window_index_str:
            raise ValueError(f"Unsupported character in input: {character}")

        letter_index = character_window_index_str[character]
        seed_index = find_seed_index(working_seed, letter_index)
        decrypted_character = character_window_inverse_index_int[seed_index]
        decrypted_word_list.append(decrypted_character)
        trace.append(
            f"[word {word_count}] {character} -> {letter_index}; "
            f"found at seed[{seed_index}] -> {decrypted_character}"
        )

    decrypted_word = "".join(decrypted_word_list)
    trace.append(f"[word {word_count}] decrypted word: {decrypted_word}")
    return decrypted_word


def rotate_seed_for_word(seed: list[str], word_count: int, trace: list[str]) -> list[str]:
    working_seed = seed[:]

    if word_count <= 1:
        trace.append(f"[word {word_count}] using base seed")
        return working_seed

    trace.append(f"[word {word_count}] rotating seed {word_count} time(s)")
    for _rotation_index in range(word_count):
        working_seed = working_seed[-1:] + working_seed[:-1]

    trace.append(f"[word {word_count}] active seed: {''.join(working_seed)}")
    return working_seed


def find_seed_index(seed: list[str], letter_index: str) -> int:
    for seed_index, seed_value in enumerate(seed):
        if letter_index == seed_value:
            return seed_index

    raise ValueError(f"Could not find letter index {letter_index} in generated seed.")


def word_contains_number(word_list: list[str]) -> bool:
    return any(character in nums for character in word_list)


def format_character_list(characters: list[str]) -> str:
    return " ".join(characters) if characters else "(none)"


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
        result, trace = process_clipper_text_with_trace(text, seed_word, mode)
    except Exception as exc:  # pragma: no cover - defensive path
        return jsonify({"error": str(exc)}), 500

    return jsonify({"result": result, "trace": trace})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
