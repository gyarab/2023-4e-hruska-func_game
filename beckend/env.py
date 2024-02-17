import os
from typing import Any, Callable, Optional, TypeVar, Dict

R = TypeVar("R")

_DOTENV: Dict[str, str] = {}


def bool_(v: str) -> bool:
    return bool(int(v))


def env(t: Callable[[Any], R], name: str, default: Optional[R] = None) -> R:
    x = os.getenv(name)
    if x is None:
        x = _DOTENV.get(name)
    if x is None:
        if default is None:
            raise ValueError(f"Environment variable {name} not found!")
        else:
            return default
    return t(x)


_ENV_FILE: str = env(str, "ENV_FILE", ".env")
if os.path.isfile(_ENV_FILE):
    with open(_ENV_FILE) as f:
        for line in f.readlines():
            split = line.strip().split("=")
            if len(split) < 2 or split[0].startswith("#"):
                continue
            _DOTENV[split[0]] = "=".join(split[1:])

DB_PASSWORD: str = env(str, "DB_PASSWORD")
DB_USER: str = env(str, "DB_USER")
DB_NAME: str = env(str, "DB_NAME")
"""
DB_HOST: str = env(str, "DB_HOST")
STRIPE_SEC: str = env(str, "STRIPE_SEC")
WEBHOOK_SEC: str = env(str, "WEBHOOK_SEC")
EMAIL: str = env(str, "EMAIL")
EMAIL_PASSWORD: str = env(str, "EMAIL_PASSWORD")
"""