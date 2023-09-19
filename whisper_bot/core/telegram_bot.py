# from whisper_bot.data_model.dm_pydantic import \
#     SaveTelegramMessageRequest
from typing import TYPE_CHECKING

from aiogram import F
from aiogram import types
from bot_base.core.telegram_bot import TelegramBot

from whisper_bot.core.app_config import WhisperTelegramBotConfig

if TYPE_CHECKING:
    from whisper_bot.core import WhisperApp


class WhisperTelegramBot(TelegramBot):
    _config_class = WhisperTelegramBotConfig
    recognized_hashtags = {"#ignore": {"ignore": True}}  #

    def __init__(self, config: _config_class, app: "WhisperApp" = None):
        super().__init__(config, app=app)

    async def process_audio(self, message: types.Message):
        self.logger.info(f"Processing audio message")

        transcript = await self._process_voice_message(message)
        # todo: add file name, if present
        response = f"Transcript: \n{transcript}"

        await self.send_safe(message.chat.id, response, message.message_id)

    async def bootstrap(self):
        self._dp.message(F.audio | F.voice)(self.process_audio)

        await super().bootstrap()

    async def chat_message_handler(self, message: types.Message):
        """
        Placeholder implementation of main chat message handler
        Parse the message as the bot will see it and send it back
        Replace with your own implementation
        """
        message_text = await self._extract_message_text(message)
        self.logger.info(f"Received message: {message_text}")
        if self._multi_message_mode:
            self.messages_stack.append(message)
        else:
            # todo: send back a 'help' message
            await message.answer(
                f"This is a whisper-bot. Send voice messages to parse them to text"
            )

        return message_text
