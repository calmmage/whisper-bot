"""
WhisperApp class
- Database for storing processed whispers and logs
-
"""
from bot_base.core import App
from bot_base.utils.gpt_utils import (
    split_by_weight,
    get_token_count,
    amap_gpt_command,
    token_limit_by_model,
)
from functools import partial
from whisper_bot.core import WhisperAppConfig
from whisper_bot.core import WhisperTelegramBot
from whisper_bot.core.app_config import WhisperTelegramBotConfig
from whisper_bot.utils.text_utils import FORMAT_TEXT_COMMAND, merge_all_chunks


class WhisperApp(App):
    _app_config_class = WhisperAppConfig
    _telegram_bot_class = WhisperTelegramBot
    _telegram_bot_config_class = WhisperTelegramBotConfig

    @property
    def formatting_model(self):
        return self.config.formatting_model

    async def merge_and_format_chunks(self, chunks):
        # step 1: group chunks by size
        self.logger.info(f"Splitting chunks by size")
        # token limit should be half of the model's token limit to fit the result
        token_limit = token_limit_by_model[self.formatting_model] / 2
        groups = split_by_weight(
            chunks, partial(get_token_count, model=self.formatting_model), token_limit
        )
        # step 2: merge chunks in each group
        self.logger.info(f"Merging chunks in each group")
        merged_groups = [
            merge_all_chunks(group, logger=self.logger) for group in groups
        ]
        # step 3: format each group
        self.logger.info(f"Formatting each group")
        formatted_groups = await amap_gpt_command(
            merged_groups, FORMAT_TEXT_COMMAND, model=self.formatting_model
        )
        # step 4: merge all groups
        self.logger.info(f"Merging all groups")
        result = merge_all_chunks(formatted_groups, logger=self.logger)

        return result
