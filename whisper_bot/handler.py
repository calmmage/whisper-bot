from bot_lib import Handler, HandlerDisplayMode

from whisper_bot.app import MyApp
from aiogram import F, Router

# from aiogram.types import Video, Audio, Voice, VideoNote


class MyHandler(Handler):
    name = "main"
    display_mode = HandlerDisplayMode.FULL
    commands = {
        "dummy_command_handler": "dummy_command",
    }

    has_chat_handler = True

    async def chat_handler(self, message, app: MyApp):
        input_str = await self.get_message_text(message)
        output_str = app.invoke(input_str)
        await self.reply_safe(message, output_str)

    async def dummy_command_handler(self, message, app: MyApp):
        output_str = app.dummy_command()
        await self.reply_safe(message, output_str)

    # region new handlers
    async def dummy_audio_handler(self, message, app: MyApp):
        output_str = "Confirming that I received the audio file."
        await self.reply_safe(message, output_str)

    async def dummy_video_handler(self, message, app: MyApp):
        output_str = "Confirming that I received the video file."
        await self.reply_safe(message, output_str)

    def setup_router(self, router: Router):
        router.message.register(
            self.dummy_audio_handler,
            F.voice | F.audio,
        )

        router.message.register(self.dummy_video_handler, F.video | F.video_note)

    # region Elementary actions
    # Idea: Simple atomic commands that do units of work
    # item 1: video to audio
    # item 2: cut audio
    # item 3: audio to text
    # item 4: merge text chunks
    # item 5: format text
    # endregion Elementary actions

    # region complete scenarios
    # item 1: user sends audio
    # item 2: user sends video
    # item 3: user sends text
    # - if after parsing recently: interpret as chatting
    # - if simple text message:
    # item 4: specific extraction commands - todos, summary etc.
    # item 5: scenario / toolkit
    # endregion complete scenarios
