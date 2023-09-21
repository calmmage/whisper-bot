# from whisper_bot.data_model.dm_pydantic import \
#     SaveTelegramMessageRequest
from typing import TYPE_CHECKING

from aiogram import F
from aiogram import types

from bot_base.core import mark_command
from bot_base.core.telegram_bot import TelegramBot

from whisper_bot.core.app_config import WhisperTelegramBotConfig
from whisper_bot.utils.text_utils import merge_all_chunks, format_text_with_gpt

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

    # ------------------------------------------------------------
    # Command 1: Merge chunks
    # ------------------------------------------------------------

    async def _extract_text_from_message(self, message: types.Message):
        if message.document:
            self.logger.info(f"Received file: {message.document.file_name}")
            text = await self._aiogram_bot.download(message.document.file_id)
            self.logger.debug(f"File downloaded: {text}")
        else:
            text = await self._extract_message_text(message)
        return text

    @mark_command("mergeChunks")
    async def merge_chunks_command(self, message: types.Message):
        """
        Merge chunks command
        """
        self.logger.info(f"Received mergeChunks command")
        # step 1: get message text
        text = await self._extract_text_from_message(message)

        # step 2: split chunks
        chunks = text.split("\n\n")

        # step 3: merge chunks
        result = await merge_all_chunks(chunks, logger=self.logger)
        self.logger.info(f"Result: {result}")

        # send back the result
        await self.send_safe(message.chat.id, result, message.message_id)

    # ------------------------------------------------------------
    # Command 2: Format text
    # ------------------------------------------------------------

    @mark_command("formatText")
    async def format_text_command(self, message: types.Message):
        """
        Format the text with GPT
        """
        self.logger.info(f"Received formatText command")

        # extract text from the message - value or file
        text = await self._extract_text_from_message(message)

        # format the text
        result = await format_text_with_gpt(text)
        self.logger.info(f"Result: {result}")

        # send back the result
        await self.send_safe(message.chat.id, result, message.message_id)

    # ------------------------------------------------------------
    # Command 3: Merge and format
    # ------------------------------------------------------------

    async def _merge_and_format_chunks(self, chunks):
        # step 1:
        # step 3: merge chunks
        result = await merge_all_chunks(chunks, logger=self.logger)
        self.logger.info(f"Result: {result}")

        # step 4: format the text
        result = await format_text_with_gpt(result)
        self.logger.info(f"Result: {result}")
        return result
