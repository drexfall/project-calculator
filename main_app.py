import json
from datetime import datetime

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.effectwidget import (EffectWidget, HorizontalBlurEffect,
                                   VerticalBlurEffect)
from kivy.uix.modalview import ModalView
from kivy.uix.screenmanager import Screen, ScreenManager, SwapTransition
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton

from history import History
from page import Page
from properties import (color, config_data, formats, hover, platform, symbol,
                        theme_image)
from settings import Settings
from widgets import ClipButtons, Date, Drop, Icon, MyBoxLayout


class Pages(ScreenManager):
    pages_list = {}

    def page_change(self, button, *args, **kwargs):
        self.current = button.text
        if platform != "android":
            self.pages_list[self.current].focus_entry()

    def __init__(self, *args, **kwargs):
        super(Pages, self).__init__(**kwargs)

        self.transition = SwapTransition(duration=0.5)

        for page_list in config_data["page_list"]:
            self.page_screen = Screen(name=page_list["mode"])
            self.page = Page(
                page_name=page_list["mode"],
                rows=page_list["row"],
                cols=page_list["col"],
                text_list=page_list["text"],
                padding=5,
            )

            if page_list["mode"] == "days":
                self.page.preview.text = 'Click on the buttons with date!'
                self.page.layout.size_change(0, 1, 2)
                self.page.layout.size_change(1, 0, 1.5)
                self.page.layout.size_change(1, 2, 1.5)
                self.page.layout.size_change(-1, -1, 0.5)
                self.page.layout.buttons[1][0].text = self.page.layout.buttons[1][
                    2
                ].text = datetime.today().strftime(config_data["format"])

                def abc(*args):
                    today = datetime.strptime(args[0].text,config_data['format']).strftime("%d %m %Y").split()
                    date = Date(
                        button=args[0],
                        year=int(today[2]),
                        month=int(today[1]),
                        day=int(today[0]),
                    )
                    date.open()
                    self.parent.parent.options_open(args[0])

                def final(*args):
                    global config_data
                    temp = config_data["format"]
                    config_data["format"] = formats[args[0].values.index(args[0].value)]
                    self.page.layout.buttons[1][0].text = datetime.strptime(self.page.layout.buttons[1][0].text,temp).strftime(config_data['format'])
                    self.page.layout.buttons[1][2].text = datetime.strptime(self.page.layout.buttons[1][2].text,temp).strftime(config_data['format'])
                    
                    json.dump(config_data, open("config.json", "w"), indent=4)

                self.page.layout.buttons[1][0].bind(on_release=abc)
                self.page.layout.buttons[1][2].bind(on_release=abc)
                self.format_drop = Drop(
                    default = datetime.today().strftime(config_data['format']),
                    title="format",
                    size_hint=(0.7, 0.9),
                    values=list(datetime.today().strftime(x) for x in formats),
                )
                self.format_drop.bind(on_dismiss=final)
                self.format_drop.bind(on_dismiss=lambda button: self.parent.parent.options_close())
                self.page.layout.buttons[4][-1].bind(on_release=self.format_drop.open)
                self.page.layout.buttons[4][-1].bind(on_release= lambda button: self.parent.parent.options_open(button))

            elif page_list["mode"] == "convert":
                self.page.preview.text = 'Go for the units!'
                self.page.layout.buttons[0][1].bind(
                    on_release=self.page.layout.quantity_drop.open
                )
                self.page.layout.buttons[1][1].bind(
                    on_release=self.page.layout.from_drop.open
                )
                self.page.layout.buttons[1][3].bind(
                    on_release=self.page.layout.to_drop.open
                )

                self.page.layout.buttons[0][
                    1
                ].text = self.page.layout.quantity_drop.values[0]
                self.page.layout.buttons[1][1].text = self.page.layout.from_drop.values[
                    0
                ]
                self.page.layout.buttons[1][3].text = self.page.layout.to_drop.values[1]

                self.page.layout.buttons[0][1].bind(
                    on_release=lambda button: self.parent.parent.options_open(button)
                )
                self.page.layout.buttons[1][1].bind(
                    on_release=lambda button: self.parent.parent.options_open(button)
                )
                self.page.layout.buttons[1][3].bind(
                    on_release=lambda button: self.parent.parent.options_open(button)
                )

            elif page_list["mode"] == "standard":
                self.page.layout.size_change(-1, 0, 2)
            elif page_list["mode"] == "scientific":
                self.page.layout.size_change(-1, 0, 2)
                self.page.layout.inverse_change(self.page.layout.buttons[0][1])
            self.page_screen.add_widget(self.page)
            self.add_widget(self.page_screen)
            self.pages_list.update({page_list["mode"]: self.page})
        if platform != "android":
            Clock.schedule_once(
                self.pages_list[config_data["page_list"][0]["mode"]].focus_entry, 2
            )


class MainScreen(EffectWidget):
    def options_open(self, button, *args, **kwargs):
        global hover
        self.effects = [HorizontalBlurEffect(size=10), VerticalBlurEffect(size=10)]
        hover[0] = False

    def options_close(self, *args, **kwargs):
        global hover
        self.effects = []
        hover[0] = True

    def settings_open(self, *args, **kwargs):
        self.effect_layout.settings.open(self.effect_layout)
        return self

    def text_halign(self, *args):
        input = self.pages.current_screen.children[0].entry
        top = (input.parent.size[1] // 3) - input.parent.parent.parent.preview.size[
            1
        ] // 2
        input.padding = [0, top]

    def __init__(self, *args, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.effect_layout = MyBoxLayout(orientation="vertical")
        self.header_buttons = MyBoxLayout(size_hint_y=0.1)
        self.header_buttons.add_widget(ClipButtons(size_hint_x=0.3))
        self.header_buttons.add_widget(MyBoxLayout(size_hint_x=0.4))
        self.header_buttons.history = Icon(icon="history", size_hint_x=0.1)
        self.header_buttons.history_modal = ModalView(size_hint=(0.9, 0.8))
        self.header_buttons.history_modal.add_widget(History(main = self))
        self.header_buttons.history.bind(
            on_release=self.header_buttons.history_modal.children[0].refresh
        )
        self.header_buttons.history.bind(
            on_release=self.header_buttons.history_modal.open
        )
        self.header_buttons.history.bind(on_release=self.options_open)
        self.header_buttons.history_modal.bind(on_dismiss=self.options_close)

        self.header_buttons.add_widget(self.header_buttons.history)
        self.pages = Pages(size_hint=(1, 0.9))

        self.effect_layout.add_widget(self.header_buttons)
        self.effect_layout.add_widget(self.pages)

        self.add_widget(self.effect_layout)

        self.effect_layout.settings = ModalView(size_hint=(0.9, 0.9))
        self.settings_page = Settings(padding=5, spacing=0)
        self.settings_page.save_buttons.save_button.bind(
            on_release=self.effect_layout.settings.dismiss
        )
        self.effect_layout.settings.add_widget(self.settings_page)
        self.effect_layout.settings.bind(on_dismiss=self.options_close)

        Clock.schedule_interval(self.text_halign, 0.1)


if __name__ == "__main__":

    class Main(MDApp):
        def build(self):
            return MainScreen()

    Main().run()
