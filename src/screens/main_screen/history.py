from kivy.app import App
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.core.window import Window

from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.fitimage import FitImage
from kivymd.uix.divider import MDDivider
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.refreshlayout import MDScrollViewRefreshLayout

from kivymd.uix.appbar import (
    MDTopAppBar,
    MDTopAppBarTitle,
    MDTopAppBarTrailingButtonContainer,
    MDActionTopAppBarButton
)

import requests
import asynckivy

from src.utils import load_token, delete_token

class HistoryScreen(MDScreen):
    history = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = 'history'

        root_layout = MDBoxLayout(orientation="vertical")

        root_layout.add_widget(
            MDTopAppBar(
                MDTopAppBarTitle(
                    text='History'
                ),
                MDTopAppBarTrailingButtonContainer(
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
            bar_width=4
        )

        self.content = MDGridLayout(
            cols=1,
            adaptive_height=True,
            padding=(dp(16), dp(16), dp(16), dp(16)),
            spacing=dp(10),
        )

        self.grid: MDGridLayout = MDGridLayout(
            cols=self.get_columns(),  # jumlah kolom dinamis
            spacing=dp(10),
            adaptive_height=True,
            pos_hint={'center_x': 0.5,'center_y': 0.5}
        )

        self.content.add_widget(self.grid)
        self.refresh_layout.add_widget(self.content)

        root_layout.add_widget(self.refresh_layout)

        self.refresh_layout.root_layout = self.grid

        self.add_widget(root_layout)
        Window.bind(size=self.on_window_resize)

    def logout(self, *args):
        delete_token()
        App.get_running_app().root.transition.direction = "down"
        App.get_running_app().root.current = "login"

    def on_pre_enter(self, *args):
        print("[DEBUG] Masuk ke tab history — fetch history")
        asynckivy.start(self.get_history())
    
    def populate_cards(self):
        self.grid.clear_widgets()

        if len(self.history) == 0:
            # Tampilkan teks "No history yet"
            self.grid.add_widget(
                MDLabel(
                    text="No history yet",
                    halign="center",
                    theme_text_color="Hint",
                    # font_style="TitleMedium",
                    size_hint_y=None,
                    height=dp(100)
                )
            )
            return

        for o in self.history:
            menu = o["menu"]
            image_url = f"https://cafe.ddns.net{menu['gambar']}"

            card = MDCard(
                orientation="vertical",
                size_hint=(1, None),
                height=dp(380),
                elevation=4,
                radius=dp(12),
            )

            # Gambar menu
            card.add_widget(
                FitImage(
                    source=image_url,
                    size_hint=(1, None),
                    height=dp(200),
                    radius=[dp(12), dp(12), 0, 0],
                )
            )

            box = MDBoxLayout(orientation="vertical", padding=dp(12), spacing=dp(4))

            # Nama menu
            box.add_widget(
                MDLabel(
                    text=menu["nama"].capitalize(),
                    # font_style="TitleMedium",
                    theme_text_color="Primary",
                    bold=True,
                    halign="left",
                )
            )

            # Status history (selesai)
            status_text = o["status"].capitalize()
            box.add_widget(
                MDLabel(
                    text=f"Status: {status_text}",
                    theme_text_color="Secondary",
                    # font_style="BodySmall",
                    halign="left",
                )
            )

            box.add_widget(MDDivider())

            # ID Pesanan
            box.add_widget(
                MDLabel(
                    text=f"ID: {o['id']}",
                    # font_style="Caption",
                    halign="left",
                    theme_text_color="Hint",
                )
            )

            card.add_widget(box)
            self.grid.add_widget(card)

    async def get_history(self):
        token, _, id = load_token()
        print('history')
        print(token, id)
        url = f'https://cafe.ddns.net/user/{id}/pesanan'
        try:
            def x():
                headers = {
                    'user-token': token
                }

                return requests.get(url, headers=headers)
            
            response = await asynckivy.run_in_thread(x)
            historyjson = response.json()
            self.history = []
            for history in historyjson.get('pesanans', []):
                if history['status'] == 'selesai':
                    self.history.append(history)

            print(self.history)
            self.populate_cards()
        except requests.exceptions.RequestException as e:
            print(f"Failed to get history: {e}")

    def refresh_callback(self, *args):
        def do_refresh(_):
            self.refresh_layout.refresh_done()
            print('relaod!')
            asynckivy.start(self.get_history())
            
            Clock.schedule_once(lambda dt: self.content.do_layout(), 0.2)

        Clock.schedule_once(do_refresh, 1)

    def get_columns(self):
        width = Window.width
        if width <= 800:
            return 2
        elif width <= 1600:
            return 3
        else:
            return 4
        
    def on_window_resize(self, instance, size):
        self.grid.cols = self.get_columns()