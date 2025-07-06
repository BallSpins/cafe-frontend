from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView

class ScrollableCardApp(MDApp):
    def build(self):
        scroll = MDScrollView()

        container = MDBoxLayout(orientation='vertical', size_hint_y=None, padding=[40, 10, 40, 10], spacing=10)
        container.bind(minimum_height=container.setter('height'))

        # Buat 10 dummy card
        for i in range(10):
            card = MDCard(
                orientation='vertical',
                size_hint=(1, None),
                height=120,
                padding=10,
                elevation=4,
            )
            card.add_widget(MDLabel(
                text=f"Card {i + 1}",
                theme_text_color="Primary",
            ))
            card.add_widget(MDLabel(
                text="Ini adalah isi dummy card.",
                theme_text_color="Secondary"
            ))

            container.add_widget(card)

        scroll.add_widget(container)
        return scroll

ScrollableCardApp().run()
