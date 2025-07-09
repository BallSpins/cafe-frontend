from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.screenmanager import MDScreenManager
from src.screens.login import LoginScreen  # Adjust the path to your login_screen.py
from src.screens.register import RegisterScreen  # Adjust the path to your register_screen.py
from src.screens.main import MainScreen  # Adjust the path to your main_screen.py

from src.utils import save_token, load_token, check_expired_token, delete_token

from kivy.config import Config
import asynckivy
from kivy.clock import Clock
# Config.set('kivy', 'window_icon', "src/img/256x256.png")  # Use system keyboard mode
class PreviewApp(MDApp):
    def build(self):
        self.icon = "src/img/256x256.png"
        self.sm = MDScreenManager()
        self.sm.add_widget(LoginScreen(name="login"))
        self.sm.add_widget(RegisterScreen(name="register"))
        self.sm.add_widget(MainScreen(name="main"))

        Clock.schedule_once(lambda dt: asynckivy.start(self.check_token()), 0)

        return self.sm
    
    async def check_token(self):
        token, created_at, id = load_token()
        if not token or await check_expired_token(created_at, token=token, id=id):
            self.sm.current = "login"
        else:
            delete_token()
            self.sm.current = "main"
    
    def get_application_name(self):
        return "Cafe App"
    
if __name__ == "__main__":
    PreviewApp().run()