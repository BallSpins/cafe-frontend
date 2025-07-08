from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import ScrollView
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivy.metrics import dp
from kivy.core.window import Window
from kivymd.uix.card import MDCard
from kivymd.uix.fitimage import FitImage
from kivymd.uix.refreshlayout import MDScrollViewRefreshLayout
from kivy.clock import Clock
from kivymd.uix.button import MDIconButton, MDButton, MDButtonText
from kivymd.uix.appbar import (
    MDTopAppBar,
    MDTopAppBarTitle,
    MDTopAppBarTrailingButtonContainer,
    MDActionTopAppBarButton
)
import requests
from src.utils import delete_token, get_cart_count_id, get_cart_items, add_cart_items, delete_cart_items, post_order
from kivy.app import App
from kivy.lang import Builder
import asynckivy

from src.helper.main_screen.home import head_wrapper
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogIcon,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
    MDDialogContentContainer,
)
from kivymd.uix.list import (
    MDListItem,
    MDListItemLeadingIcon,
    MDListItemSupportingText,
    MDListItemHeadlineText
)
from kivymd.uix.divider import MDDivider
from kivymd.uix.card import MDCard

class HomeScreen(MDScreen):
    menu = []

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
                        icon='cart',
                        on_release=self.open_cart
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
            bar_width=4
        )

        self.content = MDGridLayout(
            cols=1,
            adaptive_height=True,
            padding=(dp(16), dp(16), dp(16), dp(16)),
            spacing=dp(10),
        )

        head_wrap = Builder.load_string(head_wrapper)

        self.content.add_widget(head_wrap)

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
        asynckivy.start(self.get_menu())
        Window.bind(size=self.on_window_resize)

    def logout(self, *args):
        delete_token()
        App.get_running_app().root.transition.direction = "down"
        App.get_running_app().root.current = "login"

    def open_cart(self, *args):
        box = MDBoxLayout(orientation="vertical", adaptive_height=True)
        self.qty_labels = {}

        for i in get_cart_items():
            menu_item = self.get_menu_item_by_id(i.menu_id)
            if menu_item is None:
                continue

            qty = get_cart_count_id(i.menu_id)

            qty_label = MDListItemSupportingText(text=f'{qty}x Rp {menu_item['harga']}')

            item_row = MDListItem(
                MDListItemHeadlineText(text=menu_item['nama'].capitalize()),
                qty_label,
                theme_bg_color="Custom",
                md_bg_color=self.theme_cls.backgroundColor,
            )

            self.qty_labels[i.menu_id] = qty_label

            controls = MDBoxLayout(
                orientation='horizontal',
                adaptive_size=True,
                spacing=dp(4)
            )

            controls.add_widget(
                MDIconButton(
                    icon='minus',
                    on_release=self.remove_from_cart(i.menu_id),
                )
            )

            controls.add_widget(
                MDIconButton(
                    icon='plus',
                    on_release=self.add_to_cart(i.menu_id),
                )
            )

            item_row.add_widget(controls)

            box.add_widget(item_row)


        scroll = ScrollView(size_hint_y=None, height="300dp")
        scroll.add_widget(box)

        bottom_bar = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            padding=(dp(16), dp(10)),
            adaptive_height=True,
        )

        self.total_label = MDLabel(
            text=f'Total: Rp {self.get_total_price()}',
            halign='left'
        )

        self.checkout_btn = MDButton(
            MDButtonText(text='Checkout'),
            on_release=self.checkout,
            pos_hint={"center_x": 0.5},
        )

        self.checkout_btn.disabled = len(get_cart_items()) == 0

        bottom_bar.add_widget(self.total_label)
        bottom_bar.add_widget(self.checkout_btn)

        container = MDBoxLayout(
            orientation='vertical',
            adaptive_height=True,
            spacing=dp(40)
        )

        container.add_widget(scroll)
        container.add_widget(bottom_bar)
        # container.add_widget(self.total_label)
        
        # Dialog
        self.dialog = MDDialog(
            MDDialogIcon(icon="cart"),
            # MDDialogHeadlineText(text="Your Cart"),
            MDDialogContentContainer(
                container,
                orientation="vertical",
            ),
        )
        self.dialog.open()

    def get_total_price(self) -> int:
        total = 0
        for item in get_cart_items():
            menu = self.get_menu_item_by_id(item.menu_id)
            count = item.quantity
            if menu:
                total += count * menu['harga']
        return total
    
    def checkout(self, *args):
        post_order()
        self.dialog.dismiss()

    def add_to_cart(self, menu_id):
        def handler(_):
            add_cart_items(menu_id)
            self.update_qty_label(menu_id)
        return handler

    def remove_from_cart(self, menu_id):
        def handler(_):
            delete_cart_items(menu_id)
            self.update_qty_label(menu_id)
        return handler

    def update_qty_label(self, menu_id):
        qty = get_cart_count_id(menu_id)
        menu_item = self.get_menu_item_by_id(menu_id)
        if menu_id in self.qty_labels and menu_item:
            self.qty_labels[menu_id].text = f'{qty}x Rp {menu_item["harga"]}'
        self.total_label.text = f'Total: Rp {self.get_total_price()}'
        self.checkout_btn.disabled = len(get_cart_items()) == 0

    def get_menu_item_by_id(self, menu_id: int):
        for item in self.menu:
            if item["id"] == menu_id:
                return item
        return None

    async def get_menu(self):
        try:
            def _():
                return requests.get('https://cafe.ddns.net/menu/')

            response = await asynckivy.run_in_thread(_)
            self.menu = response.json()
            self.populate_cards()
        except requests.exceptions.RequestException as e:
            print(f"Failed to get menu: {e}")

    def populate_cards(self):
        self.grid.clear_widgets()
        # Tambahkan contoh menu
        for item in self.menu:
            card = MDCard(
                orientation='vertical',
                size_hint=(1, None),
                height=dp(300),
                elevation=4,
                radius=dp(12)
            )

            box = MDBoxLayout(
                orientation='vertical',
                padding=dp(15)
            )

            wrapper = MDBoxLayout(
                orientation='horizontal'
            )

            wrapper.add_widget(
                MDLabel(
                    text=f"{item['nama'].capitalize()}",
                    halign='left'
                )
            )

            wrapper.add_widget(
                MDLabel(
                    text=f'Rp {item['harga']}',
                    halign='right'
                )
            )

            box.add_widget(wrapper)

            box.add_widget(
                MDButton(
                    MDButtonText(text='Add to cart'),
                    on_release=lambda _, _id=item['id']: add_cart_items(_id),
                    disabled=False if item['status'] == 'TERSEDIA' else True
                )
            )

            # box.add_widget(MDLabel(
            #     text=f"Status: {item['status']}",
            #     theme_text_color="Secondary"
            # ))

            # Tambahkan gambar
            card.add_widget(
                FitImage(
                    source=f"https://cafe.ddns.net{item['gambar']}",
                    size_hint_y=None,
                    height=dp(200),
                    radius=[dp(8), dp(8), 0, 0],
                )
            )
            card.add_widget(box)

            self.grid.add_widget(card)

    def refresh_callback(self, *args):
        def do_refresh(_):
            self.refresh_layout.refresh_done()
            print('relaod!')
            asynckivy.start(self.get_menu())
            
            Clock.schedule_once(lambda dt: self.content.do_layout(), 0.2)

        Clock.schedule_once(do_refresh, 1)

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
