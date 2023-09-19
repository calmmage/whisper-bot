# run the app
from bot_base.data_model.mongo_utils import connect_to_db
from bot_base.utils.logging_utils import setup_logger
from whisper_bot.core.app import WhisperApp
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    # connect to db
    connect_to_db()

    # setup logger
    setup_logger()

    app = WhisperApp()
    app.run()
