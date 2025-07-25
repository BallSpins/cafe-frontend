from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from src.helper.login import Label, Buttons, Textfields

import requests

from kivy.core.window import Window
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField, MDTextFieldTrailingIcon
from kivymd.uix.snackbar import (
    MDSnackbar,
    MDSnackbarText,
)
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.anchorlayout import MDAnchorLayout

from src.utils import save_token
from kivy.metrics import dp

class LoginScreen(MDScreen):
    """
    This class represents the login screen of the application.
    It inherits from MDScreen, which is a part of KivyMD.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = self.theme_cls.backgroundColor

        login_label: MDLabel = Builder.load_string(Label)

        button_layout: MDGridLayout = Builder.load_string(Buttons)

        login_button: MDButton = button_layout.children[1]
        register_button = button_layout.children[0]

        login_button.on_release = self.show_data
        register_button.on_release = self.go_to_register

        textfield_layout: MDAnchorLayout = Builder.load_string(Textfields)
        self.email: MDTextField = textfield_layout.children[0].children[1]
        self.password: MDTextField = textfield_layout.children[0].children[0]

        main_layout = MDGridLayout(
            cols=1,
            size_hint=(0.9, None),
            adaptive_width=True,
            adaptive_height=True,
            spacing='96dp', 
            padding='16dp',
            pos_hint={'center_x': 0.5, 'center_y': 0.4}
        )
        
        main_layout.add_widget(login_label)
        main_layout.add_widget(textfield_layout)
        main_layout.add_widget(button_layout)

        self.add_widget(main_layout)

        def on_window_resize(window, size):
            width, height = size
            self.current_screen_width = width
            print(f'Current screen width: {self.current_screen_width}')
        Window.bind(size=on_window_resize)

    def reset_form(self, *args):
        """
        This method is used to reset the form fields.
        It is called when the user clicks the reset button.
        """
        self.email.text = ""
        self.password.text = ""

    def go_to_register(self, *args):
        self.reset_form()
        self.manager.transition.direction = "left"
        self.manager.current = "register"

    def send_request(self, *args):
        response = requests.post(
            'https://cafe.ddns.net/auth/user/login',
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
                },
            json={
                'email': self.email.text,
                'password': self.password.text
            }
        )

        print(response.status_code, response.text)

        if response.status_code != 200:
            snackbar: MDSnackbar = MDSnackbar(
                MDSnackbarText(
                    text="Login failed. Please try again.",
                    theme_text_color="Error"
                ),
                y='24dp',
                pos_hint={"center_x": 0.5},
                size_hint_x=0.8,
                background_color=self.theme_cls.backgroundColor,
            )
            snackbar.open()
            return
        else:
            self.reset_form()
            token = response.json().get('token')
            user_id = response.json().get('user_id')
            save_token(token, user_id)
            self.manager.transition.direction = "up"
            self.manager.current = "main"
        
    def show_data(self, *args):
        email: str = self.email.text
        password: str = self.password.text
        if not email or not password:
            self.not_dialog()
            return
        
        self.send_request()
        # self.on_details(email, password)
        
        print(f'Username: {email}, Password: {password}')
    
    def not_dialog(self, *args):
        """
        This method is used to show a dialog when the user does not enter any data.
        It is called when the user clicks the login or register button without entering any data.
        """
        snackbar: MDSnackbar = MDSnackbar(
            MDSnackbarText(
                text="Please enter email and password.",
                theme_text_color="Error"
            ),
            y='24dp',
            pos_hint={"center_x": 0.5},
            size_hint_x=0.8,
            background_color=self.theme_cls.backgroundColor,
        )
        snackbar.open()
