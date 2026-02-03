from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent / "jwt"


def load_private_key() -> str:
    with open(BASE_DIR / "private.pem", "r") as f:
        return f.read()

def load_public_key() -> str:
    with open(BASE_DIR / "public.pem", "r") as f:
        return f.read()

ALGORITHM = "RS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 1
PRIVATE_KEY = load_private_key()
PUBLIC_KEY = load_public_key()