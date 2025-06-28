import json
import os
import sys
import webbrowser

from kivy.clock import Clock
from kivy.core.text import markup
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.lang.builder import Builder
from kivy.metrics import dp
from kivy.properties import (
    BooleanProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    StringProperty,
)
from kivy.uix.scrollview import ScrollView
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivymd.app import MDApp
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.selectioncontrol import MDCheckbox, MDSwitch
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.swiper import MDSwiper
from kivymd.uix.textfield import MDTextField

from properties import color, config_data, theme_image
from widgets import Container, ListItem, MButton, MLabel, MyBoxLayout, Swiper, TextField

Builder.load_string(
    """
#:import MButton widgets.MButton

[Panel@MButton]:
    text: ctx.title
    modal_button: True
    canvas.before:
        PushMatrix
        Translate:
            xy: self.center_x, self.center_y
        Rotate:
            angle: 90 if ctx.item.orientation == 'horizontal' else 0
            axis: 0, 0, 1
        Translate:
            xy: -self.center_x, -self.center_y
    canvas.after:
        PopMatrix
            """
)


class SwitchText(BoxLayout):
    option = ObjectProperty(MDCheckbox)
    index = NumericProperty()
    down = BooleanProperty()

    def touch(self, button):
        final = int(self.setting_button.active)
        self.parent.parent.parent.parent.selected.update(
            {list(self.parent.parent.parent.parent.selected.keys())
             [self.index]: final}
        )

    def __init__(self, **kwargs):
        super(SwitchText, self).__init__(**kwargs)
        self.button_box = BoxLayout()
        self.setting_button = self.option(size_hint=(None, None),
                                          size=(45, 45),
                                          selected_color=color(
                                              f"images/{theme_image[config_data['theme']][2]}.png"),
                                        unselected_color = color(f"images/{theme_image[config_data['theme']][0]}.png")
                                          )
        self.setting_button.update_color()
        self.setting_button.update_primary_color(
            self, color(f"images/{theme_image[config_data['theme']][1]}.png")
        )

        if self.down:
            self.setting_button.state = "down"
        self.setting_button.bind(on_release=self.touch)
        self.add_widget(self.setting_button)


class SaveButtons(MyBoxLayout):
    def apply_func(self, *args, **kwargs):
        global config_data
        for x in self.parent.accordion.children:
            if type(x.box).__name__ == "General":
                config_data.update(x.box.selected)
            elif type(x.box).__name__ == "Themes":
                new = list(theme_image.keys())[x.box.image_item.get_items().index(x.box.active_theme.parent.parent)]
                if new != config_data["theme"]:
                    config_data.update({"theme": new})
                    x.box.theme_active.text = (
                        f"{new} is applied!"
                    )
                    x.box.restart_text.text = "Click on restart to see the changes!"
                    self.save_button.text = "Restart"

    def save_func(self, *args, **kwargs):
        self.apply_func()
        with open("config.json", "r+") as config_file:
            data = json.load(config_file)
            for x in self.parent.accordion.children:
                if type(x.box).__name__ == "General":
                    data.update(x.box.selected)
                elif type(x.box).__name__ == "Themes":
                    data.update({"theme": config_data["theme"]})

            config_file.seek(0)
            config_file.truncate(0)
            json.dump(data, config_file, indent=4)
        if self.save_button.text == "Restart":
            os.execl(sys.executable, sys.executable, *sys.argv)

    def __init__(self, **kwargs):
        super(SaveButtons, self).__init__(**kwargs)
        self.apply_button = MButton(text="Apply", modal_button=True)
        self.apply_button.bind(on_release=self.apply_func)
        self.save_button = MButton(text="Save", modal_button=True)
        self.save_button.bind(on_release=self.save_func)
        self.add_widget(self.apply_button)
        self.add_widget(self.save_button)


class General(MyBoxLayout):
    selected = {
        "base": config_data["base"],
        "inverse": config_data["inverse"],
        "radian": config_data["radian"],
        "history_length": config_data["history_length"],
        "splash": config_data["splash"],
    }

    def __init__(self, **kwargs):
        super(General, self).__init__(**kwargs)
        for index, option_tuple in enumerate(
            (
                (
                    "math-compass",
                    "Set the base",
                    "for logarithmic calculations",
                    "base",
                ),
                (
                    "math-sin",
                    "Inverse on start",
                    "keep Inverse toggle on when starting the application",
                ),
                (
                    "angle-acute",
                    "Radian on start",
                    "keep Radian toggle on when starting the application",
                ),
                (
                    "history",
                    "History length",
                    "the latest entry will replace the oldest entry",
                    "history_length",
                ),
                (
                    "image-outline",
                    "Splash screen",
                    "turning this off won't affect the loading time",
                    "splash",
                ),
            )
        ):

            container = Container(
                padding=[0, 0, dp(20), 0] if index in [1, 2, 4] else [0] * 4
            )
            if index in [1, 2, 4]:
                container.add_widget(
                    SwitchText(
                        index=index,
                        down=True
                        if self.selected[list(self.selected.keys())[index]] == 1
                        else False)
                )
            else:
                container.add_widget(
                    TextField(
                        text=str(self.selected[option_tuple[3]]),
                        title=option_tuple[3],
                        halign="center",
                        multiline=False
                    )
                )
                input = container.children[0]
                input.bind(
                    on_text_validate=lambda input=input, **kwargs: self.selected.update(
                        {input.title: input.text}
                    )
                )

            self.setting_option = ListItem(
                icon=option_tuple[0],
                text=option_tuple[1],
                secondary_text=option_tuple[2],
                container=container,
                width_mult=0.5 if index in [1, 2, 4] else 0.6,
            )

            self.setting_option.add_widget(container)
            self.add_widget(self.setting_option)

        self.add_widget(MyBoxLayout(size_hint_y=0.3))


class Themes(MyBoxLayout):
    theme_check = ListProperty()
    active_theme = ObjectProperty()
    items = ListProperty()

    def on_theme_swipe(self, *args):

        for item in self.items:

            if item == args[0].get_current_item():
                item.hover = True
                item.layout.image_container.elevation = 5
                item.on_enter()
                Clock.schedule_once(item.on_leave, 1.5)
            else:
                item.on_leave()
                item.layout.image_container.elevation = 0
                item.hover = False

    def theme(self, *args):
        c = 0
        
        for x in self.theme_check:
            if x.state == "down":
                c += 1
        if c != 1:
            self.active_theme.state = "down"
        elif c == 1:
            for x in self.theme_check:
                if x.state == "down":
                    self.active_theme = x

    def __init__(self, **kwargs):
        super(Themes, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.selector = MyBoxLayout(padding=dp(10))
        self.image_item = MDSwiper(
            swipe_distance=dp(40), size_hint_y=None, height=dp(200), width_mult=6
        )
        self.image_item.bind(on_swipe=lambda a: self.on_theme_swipe(a))
        for x, name in enumerate([j for j in theme_image]):
            self.item = Swiper(source=str(x + 1), title=name)
            if name == config_data["theme"]:
                self.item.layout.select.active = self.item.hover = True

            self.theme_check.append(self.item.layout.select)
            self.image_item.add_widget(self.item)
        self.theme()
        self.items = self.image_item.get_items()
        self.selector.add_widget(self.image_item)

        self.add_widget(MyBoxLayout(size_hint_x=0.1))
        self.add_widget(self.selector)
        self.image_item.set_current(list(theme_image.keys()).index(config_data["theme"]))

        self.theme_active = MLabel(
            text=f"{self.active_theme.parent.parent.title} is applied!"
        )
        self.add_widget(self.theme_active)

        self.restart_text = MLabel(size_hint_y=0.4)
        self.add_widget(self.restart_text)
        Window.bind(
            on_key_up=lambda *args: self.image_item.swipe_left()
            if args[2] == 80
            else self.image_item.swipe_right()
        )


class About(MyBoxLayout):
    font_size = NumericProperty(14)

    def __init__(self, **kwargs):
        super(About, self).__init__(**kwargs)
        self.padding = [75, 30]
        self.header = MLabel(
            text="Calculator",
            valign="top",
            bold=True,
            font_size=dp(self.font_size*1.5),
            size_hint_y=0.6,
        )
        first_line = "This project was made keeping the power of [ref=https://www.python.org/][b]Python[/b][/ref] and flexibillity of open source software in mind. "
        second_line = "We have strived to bring you the richness of [ref=https://material.io/design][b]Google's Material Design[/b][/ref] via [ref=https://kivy.org/#home][b]Kivy[/b][/ref] and [ref=https://kivymd.readthedocs.io/en/latest/][b]KivyMD[/b][/ref] "
        third_line = "alongwith the good old [ref=https://python-pillow.org/][b]Pillow[/b][/ref] and [ref=https://docs.python.org/3/library/math.html][b]Math[/b][/ref] libraries. "
        fourth_line = "\n\nHope you have a great time with this completely free and open source application! "
        self.body1 = MLabel(
            text=first_line+second_line+third_line+fourth_line,
            markup=True,
            font_size=dp(self.font_size*1),
            halign='justify',
            valign="top"
        )

        self.footer = MyBoxLayout()
        credit_text1 = "[ref=https://www.pexels.com/photo/black-and-grey-casio-scientific-calculator-showing-formula-220301/][b]splash image[/b][/ref]"
        credit_text2 = "[ref=https://www.iconarchive.com/show/button-ui-system-apps-icons-by-blackvariant/Calculator-icon.html][b]app icon[/b][/ref]"
        credit_text3 = "[ref=https://github.com/fawazahmed0/exchange-api][b]currency API[/b][/ref]"
        self.footer.splash_credit = MLabel(

            text=credit_text1+'\n'+credit_text2+'\n'+credit_text3,
            markup=True,
            font_size=dp(self.font_size*0.8),
            valign="bottom",
            halign="left",
            size_hint=(0.4, 1),
        )

        self.footer.source_code = MLabel(
            text="[ref=https://www.github.com/shreyash/project-calculator][b]by drexfall[/b][/ref]",
            font_size=dp(self.font_size*0.9),
            valign="bottom",
            halign="center",
            markup=True,
            size_hint=(0.2, 1)
        )
        social_text1 = "[ref=https://www.instagram.com/drexfall/][b]instagram[/b][/ref]"
        social_text2 = "[ref=https://in.linkedin.com/in/drexfall/][b]linkedin[/b][/ref]"
        social_text3 = "[ref=https://www.github.com/drexfall/][b]github[/b][/ref]"
        self.footer.socials = MLabel(

            text=social_text1 + '\n' + social_text2 + '\n' + social_text3,
            markup=True,
            font_size=dp(self.font_size * 0.8),
            valign="bottom",
            halign="right",
            size_hint=(0.4, 1),
        )

        self.footer.add_widget(self.footer.splash_credit)
        self.footer.add_widget(self.footer.source_code)
        self.footer.add_widget(self.footer.socials)

        self.footer.source_code.bind(
            on_ref_press=lambda args, args1: webbrowser.get().open_new_tab(args1)
        )
        self.footer.splash_credit.bind(
            on_ref_press=lambda args, args1: webbrowser.get().open_new_tab(args1)
        )
        self.body1.bind(
            on_ref_press=lambda args, args1: webbrowser.get().open_new_tab(args1)
        )
        self.footer.socials.bind(
            on_ref_press=lambda args, args1: webbrowser.get().open_new_tab(args1)
        )

        self.add_widget(self.header)
        self.add_widget(self.body1)
        self.add_widget(self.footer)


class Settings(MyBoxLayout):
    def __init__(self, *args, **kwargs):
        super(Settings, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.accordion = Accordion(orientation="vertical")
        for x in [General, Themes, About]:
            item = AccordionItem(title=str(x.__name__), title_template="Panel")
            item.box = x(orientation="vertical")
            item.add_widget(item.box)
            self.accordion.add_widget(item)

        for x in self.accordion.children:
            x.collapse = False if type(x.box).__name__ == "General" else True

        self.add_widget(self.accordion)
        self.save_buttons = SaveButtons(size_hint_y=0.1)
        self.add_widget(self.save_buttons)


class Main(MDApp):
    def build(self):
        return Settings()


if __name__ == "__main__":
    Main().run()
