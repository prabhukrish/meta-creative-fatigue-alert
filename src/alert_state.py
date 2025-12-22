import json
from datetime import datetime, timedelta
from pathlib import Path

STATE_FILE = Path("alert_state.json")
COOLDOWN_HOURS = 48


def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def should_alert(ad_id):
    state = load_state()

    last_alert_str = state.get(ad_id)
    if not last_alert_str:
        return True

    last_alert_time = datetime.fromisoformat(last_alert_str)
    if datetime.utcnow() - last_alert_time >= timedelta(hours=COOLDOWN_HOURS):
        return True

    return False


def record_alert(ad_id):
    state = load_state()
    state[ad_id] = datetime.utcnow().isoformat()
    save_state(state)
