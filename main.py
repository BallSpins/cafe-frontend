from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.screenmanager import MDScreenManager
from src.screens.login import LoginScreen  # Adjust the path to your login_screen.py
from src.screens.register import RegisterScreen  # Adjust the path to your register_screen.py

from kivy.config import Config
# Config.set('kivy', 'window_icon', "src/img/256x256.png")  # Use system keyboard mode
class PreviewApp(MDApp):
    def build(self):
        self.icon = "src/img/256x256.png"
        sm = MDScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(RegisterScreen(name="register"))

        sm.bind(current=self.on_screen_change)
        sm.current = "login"  # Set the initial screen to login
        self.title = "Login Screen"

        return sm
    
    def on_screen_change(self, instance, value):
        if value == "login":
            self.title = "Login Screen"
        elif value == "register":
            self.title = "Register Screen"
    
if __name__ == "__main__":
    PreviewApp().run()