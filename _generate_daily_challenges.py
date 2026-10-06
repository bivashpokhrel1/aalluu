"""PuzzleVault backend — Flask server for room sync and daily puzzles."""

import random
import string
from datetime import datetime

from flask import Flask, jsonify

app = Flask(__name__)

# ── Puzzle templates ──────────────────────────────────────────────────────

PUZZLE_TYPES = ["wire_circuit", "keypad", "grid_slide", "sequence", "pattern_match"]


def _generate_daily_challenges():
    today = datetime.utcnow().strftime("%Y%m%d")
    rng = random.Random(int(today))
    challenges = []
    for i, ptype in enumerate(rng.sample(PUZZLE_TYPES, len(PUZZLE_TYPES))):
        base_time = {"wire_circuit": 120, "keypad": 90, "grid_slide": 150,
                     "sequence": 60, "pattern_match": 100}[ptype]
        challenges.append({
            "id": f"daily_{today}_{i}",
            "type": ptype,
            "seed": rng.randint(1000, 9999),
            "base_time_limit_sec": base_time,
            "date": today,
        })
    return challenges


# ── Routes ────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return jsonify({"status": "PuzzleVault API Live"})


@app.route("/api/room/create", methods=["POST"])
def create_room():
    code = "PV-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return jsonify({"room_code": code})


@app.route("/api/daily")
def daily():
    return jsonify(_generate_daily_challenges())


# ── Entry point ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)