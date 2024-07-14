from calmapp import App


class MyApp(App):
    """This is an amazing application that I developed in my free time! For now it just exists, and that is good!"""

    name: str = "My amazing app"
    # Sample
    start_message = "Hello! I am {name}. {description}"
    # Sample help message
    help_message = "Help! I need somebody! Help! Not just anybody! Help! You know I need someone! Help!"

    @property
    def description(self):
        return self.__doc__

    def invoke(self, input_str):
        return input_str

    def dummy_command(self):
        return "Hey! I am a dummy"
