from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivy.metrics import dp
from kivy.core.window import Window
from kivymd.uix.card import MDCard
from kivymd.uix.fitimage import FitImage
from kivymd.uix.refreshlayout import MDScrollViewRefreshLayout
from kivy.clock import Clock
import time
from kivymd.uix.appbar import (
    MDTopAppBar,
    MDTopAppBarTitle,
    MDTopAppBarTrailingButtonContainer,
    MDActionTopAppBarButton
)
import requests
from src.utils import delete_token
from kivy.app import App

class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "home"

        root_layout = MDBoxLayout(orientation="vertical")

        root_layout.add_widget(
            MDTopAppBar(
                MDTopAppBarTitle(
                    text='Home'
                ),
                MDTopAppBarTrailingButtonContainer(
                    MDActionTopAppBarButton(
                        icon='cart'
                    ),
                    MDActionTopAppBarButton(
                        icon='logout',
                        on_release=self.logout
                    ),
                ),
                type='small'
            )
        )

        self.refresh_layout = MDScrollViewRefreshLayout(
            refresh_callback=self.refresh_callback,
            spinner_color="red",
            circle_color="white"
        )

        # Isi scroll, layout vertikal
        content = MDBoxLayout(orientation="vertical", size_hint_y=None, padding=(dp(16), dp(16), dp(16), dp(16)), spacing=dp(10))
        content.bind(minimum_height=content.setter("height"))

        head_wrapper = MDBoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(80),
            padding=(0, dp(20))
        )

        # Label yang kamu mau
        headlabel = MDLabel(
            text="Welcome to Cafe App!",
            halign='left',
            font_style="Headline",
            role="large",
            size_hint_y=None,
            height=dp(40),
        )

        head_wrapper.add_widget(headlabel)

        content.add_widget(head_wrapper)

        self.grid: MDGridLayout = MDGridLayout(
            cols=self.get_columns(),  # jumlah kolom dinamis
            spacing=dp(10),
            adaptive_height=True,
            pos_hint={'center_x': 0.5,'center_y': 0.5}
        )

        self.populate_cards()

        content.add_widget(self.grid)
        self.refresh_layout.add_widget(content)

        root_layout.add_widget(self.refresh_layout)
        self.refresh_layout.root_layout = root_layout

        self.add_widget(root_layout)

        Window.bind(size=self.on_window_resize)

    def logout(self, *args):
        delete_token()
        App.get_running_app().root.transition.direction = "down"
        App.get_running_app().root.current = "login"

    def populate_cards(self):
        # Tambahkan contoh menu
        for i in range(10):
            card = MDCard(
                orientation='vertical',
                size_hint=(1, None),
                height=dp(300),
                # padding=dp(10),
                elevation=4,
                radius=dp(12)
            )

            box = MDBoxLayout(
                orientation='vertical',
                padding=dp(15)
            )
            box.add_widget(MDLabel(
                text=f"Card {i + 1}",
                theme_text_color="Primary",
            ))
            box.add_widget(MDLabel(
                text="Ini adalah isi dummy card.",
                theme_text_color="Secondary"
            ))

            # Tambahkan gambar
            card.add_widget(
                FitImage(
                    source=f"https://picsum.photos/300/150?random={i}&ts={int(time.time()*1000)}",
                    size_hint_y=None,
                    height=dp(200),
                    radius=[dp(8), dp(8), 0, 0],
                )
            )
            card.add_widget(box)

            self.grid.add_widget(card)

    def refresh_callback(self, *args):
        def do_refresh(_):
            print('relaod!')
            self.grid.clear_widgets()
            self.populate_cards()
            self.refresh_layout.refresh_done()

        Clock.schedule_once(do_refresh, 1.2)

    def get_columns(self):
        width = Window.width
        if width <= 400:
            return 1
        elif width <= 800:
            return 2
        elif width <= 1200:
            return 3
        else:
            return 4
        
    def on_window_resize(self, instance, size):
        self.grid.cols = self.get_columns()
