import pytest
from whisper_bot.core.app import WhisperApp


@pytest.fixture(scope="function")
def setup_environment(monkeypatch):
    monkeypatch.setenv("DATABASE_CONN_STR", "")
    monkeypatch.setenv("DATABASE_NAME", "test_db")
    monkeypatch.setenv(
        "TELEGRAM_BOT_TOKEN", "1234567890:aaabbbcccdd-aaabbbcccdddeee_abcdefg"
    )
    monkeypatch.setenv("OPENAI_API_KEY", "sk-1234567890")


def test_app(setup_environment):
    app = WhisperApp()
