"""
WhisperApp class
- Database for storing processed whispers and logs
-
"""
from bot_base.core import App
from whisper_bot.core import WhisperTelegramBot

from whisper_bot.core import WhisperAppConfig


class WhisperApp(App):
    _app_config_class = WhisperAppConfig
    _telegram_bot_class = WhisperTelegramBot
