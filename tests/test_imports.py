def test_imports():
    from whisper_bot.handler import MyHandler
    from whisper_bot.app import MyApp

    assert MyApp
    assert MyHandler
