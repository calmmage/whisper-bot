from bot_lib import Handler, HandlerDisplayMode

from whisper_bot.app import MyApp


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
        await self.reply_safe(output_str, message)

    async def dummy_command_handler(self, message, app: MyApp):
        output_str = app.dummy_command()
        await self.reply_safe(output_str, message)

    # region new handlers
    async def dummy_audio_handler(self, message, app: MyApp):
        output_str = "Confirming that I received the audio file."
        await self.reply_safe(output_str, message)

    async def dummy_video_handler(self, message, app: MyApp):
        output_str = "Confirming that I received the video file."
        await self.reply_safe(output_str, message)
