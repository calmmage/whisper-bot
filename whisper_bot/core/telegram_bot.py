from aiogram import F
from aiogram import types
from datetime import datetime
from textwrap import dedent
from typing import TYPE_CHECKING

from bot_base.core import mark_command
from bot_base.core.telegram_bot import TelegramBot
from whisper_bot.core.app_config import WhisperTelegramBotConfig
from whisper_bot.utils.text_utils import (
    merge_all_chunks,
    format_text_with_gpt,
)

if TYPE_CHECKING:
    from whisper_bot.core import WhisperApp


class WhisperTelegramBot(TelegramBot):
    _config_class = WhisperTelegramBotConfig
    app: "WhisperApp"
    recognized_hashtags = {"#ignore": {"ignore": True}}  #
    UNAUTHORISED_RESPONSE = dedent(
        """
        You are not authorized to use this bot.
        Ask @petr_lavrov for access.
        """
    )

    def __init__(self, config: _config_class, app: "WhisperApp" = None):
        super().__init__(config, app=app)

    async def process_audio(self, message: types.Message):
        self.logger.info(f"Processing audio message")
        # todo: add an easter egg - add general 'easter egg' feature everywhere
        placeholder = await message.answer(f"Transcribing audio")
        chunks = await self._process_voice_message(
            message,
        )
        raw_transcript = "\n\n".join(chunks)
        self.logger.info(f"Raw transcript: {raw_transcript}")
        filename = "raw_transcript_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        await self.send_safe(
            message.chat.id, raw_transcript, message.message_id, filename=filename
        )

        if self.config.format_transcript_automatically:
            transcript = await self.app.merge_and_format_chunks(chunks)
            filename = f"transcript_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
            await self.send_safe(
                message.chat.id, transcript, message.message_id, filename=filename
            )

        await placeholder.delete()

    # ------------------------------------------------------------
    # Command 1: Merge chunks
    # ------------------------------------------------------------

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

    @mark_command("merge_chunks")
    async def merge_chunks_command(self, message: types.Message):
        """
        Merge chunks command
        """
        self.logger.info(f"Received merge_chunks command")
        # step 1: get message text
        text = await self._extract_text_from_message(message)

        # step 2: split chunks
        chunks = text.split("\n\n")

        # step 3: merge chunks
        result = merge_all_chunks(chunks, logger=self.logger)
        self.logger.info(f"Result: {result}")

        # send back the result
        filename = f"merged_text_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        await self.send_safe(
            message.chat.id, result, message.message_id, filename=filename
        )

    # ------------------------------------------------------------
    # Command 2: Format text
    # ------------------------------------------------------------

    @mark_command("format_text")
    async def format_text_command(self, message: types.Message):
        """
        Format the text with GPT
        """
        self.logger.info(f"Received format_text command")

        # extract text from the message - value or file
        text = await self._extract_text_from_message(message)

        # format the text
        result = await format_text_with_gpt(
            text,
            model=self.app.config.formatting_model,
            fix_grammar_and_typos=self.app.config.fix_grammar_and_typos,
            logger=self.logger,
        )
        self.logger.info(f"Result: {result}")

        # send back the result
        filename = f"formatted_text_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        await self.send_safe(
            message.chat.id, result, message.message_id, filename=filename
        )

    @mark_command("fix_grammar")
    async def fix_grammar_command(self, message: types.Message):
        self.logger.info(f"Received fix_grammar command")

        # extract text from the message - value or file
        text = await self._extract_text_from_message(message)

        # format the text
        result = await format_text_with_gpt(
            text,
            model=self.app.config.formatting_model,
            fix_grammar_and_typos=True,
            logger=self.logger,
        )
        self.logger.info(f"Result: {result}")

        # send back the result
        filename = f"formatted_text_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        await self.send_safe(
            message.chat.id, result, message.message_id, filename=filename
        )

    # ------------------------------------------------------------
    # Command 3: Merge and format
    # ------------------------------------------------------------

    @mark_command("merge_and_format")
    async def merge_and_format_command(self, message: types.Message):
        # step 1: extract text from the message - value or file
        text = await self._extract_text_from_message(message)

        # step 2: split chunks
        chunks = text.split("\n\n")

        # step 3: merge chunks
        result = await self.app.merge_and_format_chunks(chunks)
        self.logger.info(f"Result: {result}")

        # send back the result
        filename = f"formatted_text_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        await self.send_safe(
            message.chat.id, result, message.message_id, filename=filename
        )

    # ------------------------------------------------------------
    # Registering handlers
    # ------------------------------------------------------------
    async def bootstrap(self):
        self._dp.message(F.audio | F.voice)(self.process_audio)
        self.register_command(self.merge_chunks_command, "merge_chunks")
        self.register_command(self.format_text_command, "format_text")
        self.register_command(self.fix_grammar_command, "fix_grammar")
        self.register_command(self.merge_and_format_command, "merge_and_format")

        await super().bootstrap()
