from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.screenmanager import MDScreenManager
from src.screens.login import LoginScreen  # Adjust the path to your login_screen.py
from src.screens.register import RegisterScreen  # Adjust the path to your register_screen.py
from src.screens.main import MainScreen  # Adjust the path to your main_screen.py

from src.utils import save_token, load_token, check_expired_token

from kivy.config import Config
# Config.set('kivy', 'window_icon', "src/img/256x256.png")  # Use system keyboard mode
class PreviewApp(MDApp):
    def build(self):
        self.icon = "src/img/256x256.png"
        sm = MDScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(RegisterScreen(name="register"))
        sm.add_widget(MainScreen(name="main"))

        token, created_at = load_token()
        if not token or check_expired_token(created_at):
            sm.current = "login"
        else:
            sm.current = "main"

        return sm
    
    def get_application_name(self):
        return "Cafe App"
    
if __name__ == "__main__":
    PreviewApp().run()