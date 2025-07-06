from kivymd.uix.screen import MDScreen
from kivy.lang import Builder

from kivy.core.window import Window
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.navigationbar import (
    MDNavigationBar,
    MDNavigationItem,
    MDNavigationItemLabel,  
    MDNavigationItemIcon,
)
from kivy.properties import StringProperty
from src.screens.main_screen.home import HomeScreen

class BaseNavItem(MDNavigationItem):
    icon = StringProperty()
    text = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(MDNavigationItemIcon(icon=self.icon))
        self.add_widget(MDNavigationItemLabel(text=self.text))

class BasePage(MDScreen):
    def __init__(self, name, **kwargs):
        super().__init__(name=name, **kwargs)
        self.add_widget(
            MDLabel(
                text=f"Ini adalah {name}",
                halign="center",
                pos_hint={"center_y": 0.5},
            )
        )

class MainScreen(MDScreen):
    """
    This class represents the main screen of the application.
    It inherits from MDScreen, which is a part of KivyMD.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_tab_index = 0
        self.md_bg_color = self.theme_cls.backgroundColor
        layout: MDBoxLayout = MDBoxLayout(orientation='vertical')

        self.screen_manager = MDScreenManager()
        self.screen_manager.add_widget(HomeScreen())
        self.screen_manager.add_widget(BasePage(name="orders"))
        self.screen_manager.add_widget(BasePage(name="history"))

        self.navbar = MDNavigationBar()
        self.navbar.bind(on_switch_tabs=self.on_switch_screen)

        self.navbar.add_widget(BaseNavItem(icon="home", text="home", active=True))
        self.navbar.add_widget(BaseNavItem(icon="clipboard-list", text="orders"))
        self.navbar.add_widget(BaseNavItem(icon="history", text="history"))

        layout.add_widget(self.screen_manager)
        layout.add_widget(self.navbar)
        self.add_widget(layout)

    
    def on_switch_screen(self, bar, item, item_icon, item_text):
        """
        Switches the current screen to the specified screen name.
        """
        print(f"Switching to screen: {item_text}")
        # Asumsikan tab diurut: home -> orders -> history
        index_map = {"home": 0, "orders": 1, "history": 2}
        last_index = self.current_tab_index
        new_index = index_map[item_text]

        # Tentukan arah transisi berdasarkan pergerakan tab
        if new_index > last_index:
            self.screen_manager.transition.direction = 'left'
        elif new_index < last_index:
            self.screen_manager.transition.direction = 'right'

        self.screen_manager.current = item_text
        self.current_tab_index = new_index

        self.screen_manager.current = item_text
        