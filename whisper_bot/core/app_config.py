from bot_base.core import AppConfig, TelegramBotConfig


class WhisperTelegramBotConfig(TelegramBotConfig):
    format_transcript_automatically: bool = True


class WhisperAppConfig(AppConfig):
    telegram_bot: WhisperTelegramBotConfig = WhisperTelegramBotConfig()

    formatting_model: str = "gpt-3.5-turbo"  # "gpt-3.5-turbo-16k" - bad quality
    summary_model: str = "gpt-4"

    fix_grammar_and_typos: bool = False
