"""
WhisperApp class
- Database for storing processed whispers and logs
-
"""
from functools import partial

from bot_base.core import App
from bot_base.utils.gpt_utils import (
    split_by_weight,
    get_token_count,
    amap_gpt_command,
    token_limit_by_model,
)
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
        token_limit = token_limit_by_model[self.formatting_model]
        groups = split_by_weight(
            chunks, partial(get_token_count, model=self.formatting_model), token_limit
        )
        # step 2: merge chunks in each group
        merged_groups = map(merge_all_chunks, groups)
        # step 3: format each group
        formatted_groups = await amap_gpt_command(
            merged_groups, FORMAT_TEXT_COMMAND, model=self.formatting_model
        )
        # step 4: merge all groups
        result = merge_all_chunks(formatted_groups)

        return result
