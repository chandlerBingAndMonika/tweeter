# careTwitter/services/token_picker.py
import os
import itertools
from typing import Callable

def load_token_names() -> list[str]:
    raw = os.getenv("TOKENS", "")
    names = [t.strip() for t in raw.split(",") if t.strip()]
    if not names:
        raise RuntimeError("No token names in TOKENS env var")
    return names

class RoundRobinTokenPicker:
    def __init__(self):
        self._names = load_token_names()
        self._cycle = itertools.cycle(self._names)

    def __call__(self, endpoint: str, user_ref: str | None = None) -> str:
        return next(self._cycle)

# 👇 זה האליאס שממנו ה-service מייבא
TokenPicker = Callable[[str, str | None], str]
