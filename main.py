from kivy.app import App
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout

from gnome_dit.constants import GNOME_DESKTOP_ICON_EXTENSION
from gnome_dit.icons import (
    action_copy_icon_to_desktop,
    get_gnome_desktop_icons,
    get_snapd_desktop_icons,
    load_icon_images,
)
from gnome_dit.schemas import UbuntuIcon


class GnomeDitApp(App):
    def __init__(self):
        super().__init__()
        self.ubuntu_icons: list[UbuntuIcon] = []
        self.icon_images = load_icon_images()

    def build(self):
        root = BoxLayout(orientation="vertical")
        scroll = ScrollView(size_hint=(1, 1))

        self.stack = StackLayout(size_hint=(1, None), spacing=15, padding=10)
        self.stack.bind(minimum_height=self.stack.setter("height"))
        scroll.add_widget(self.stack)
        root.add_widget(scroll)

        self.populate_icons()
        self.draw_icons_to_screen()

        return root

    def draw_icons_to_screen(self):
        for icon in self.ubuntu_icons:
            icon_box = BoxLayout(
                orientation="vertical",
                spacing=5,
                size_hint=(None, None),
                size=(180, 200),
            )
            # load icons as button background image
            icon_button = Button(
                size_hint=(1, 0.8),
                background_normal=icon.image_location,
                on_press=lambda instance, icon=icon: self.action_add_desktop_icon(
                    instance, icon
                ),
            )
            icon_label = Label(
                text=icon.name.removesuffix(GNOME_DESKTOP_ICON_EXTENSION),
                size_hint=(1, 0.2),
                font_size=sp(14),
            )
            icon_box.add_widget(icon_button)
            icon_box.add_widget(icon_label)
            self.stack.add_widget(icon_box)

    def action_add_desktop_icon(self, instance, icon):
        action_copy_icon_to_desktop(icon)

    def populate_icons(self):
        self.ubuntu_icons = get_gnome_desktop_icons(
            self.icon_images
        ) + get_snapd_desktop_icons(self.icon_images)


if __name__ == "__main__":
    GnomeDitApp().run()
