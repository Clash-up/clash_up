import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


class Settings:
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", 8000))

    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "clash_up")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "clash_up")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "clash_up")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", 5432))
    POSTGRES_URL: str = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

    TEST_ASYNC_DATABASE_URL: str = os.getenv(
        "TEST_ASYNC_DATABASE_URL", "sqlite+aiosqlite:///:memory:"
    )

    COC_TOKEN: str = os.getenv("COC_TOKEN", "")
    CLAN_TAG: str = os.getenv("CLAN_TAG", "#2GLCVU9QV")  # default: spacerniaki clan

    # in minutes
    POLLING_PLAYER_SYNC: int = int(os.getenv("POLLING_PLAYER_SYNC", 15))  # default: 15 minutes


settings = Settings()
