from bot_base.core import AppConfig, DatabaseConfig, TelegramBotConfig


class WhisperDatabaseConfig(DatabaseConfig):
    pass


class WhisperTelegramBotConfig(TelegramBotConfig):
    pass


class WhisperAppConfig(AppConfig):
    _database_config_class = WhisperDatabaseConfig
    _telegram_bot_config_class = WhisperTelegramBotConfig
