import json

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import RiseInTransition, Screen, ScreenManager
from kivy.utils import platform
from kivymd.app import MDApp
from kivymd.uix.progressbar import MDProgressBar
from kivymd.utils.fitimage import FitImage


class Main(MDApp):
    def resize(self, *args):
        if args[1] < dp(400):
            args[0].size = dp(400), args[2]
        if args[2] < dp(700):
            args[0].size = args[1], dp(700)

    def load(self, *args):
        from main_app import MainScreen

        self.main = Screen(name="main")
        self.main.add_widget(MainScreen())
        self.final.add_widget(self.main)
        Window.bind(on_resize=self.resize)

    def main_load(self, *args):

        temp = Window.left + dp(125), Window.top
        if platform != "android" and self.config["splash"] != 0:
            self.final.current = "main"

        def change(dt):
            Animation(
                size=(dp(500), Window.size[1]),
                left=temp[0],
                duration=0.4,
                t="in_out_cubic",
            ).start(Window)
            Window.borderless = 0

        Clock.schedule_once(change, 1.5)

    def build(self):
        Window.borderless = 1
        self.layout = RelativeLayout()
        self.final = ScreenManager()
        self.splash = Screen(name="splash")
        self.splash_image = FitImage(
            source="splash1.png",
            size=(dp(1280), dp(720)),
            radius=[
                10,
            ],
            mipmap=True,
        )
        self.layout.add_widget(self.splash_image)
        self.bar = MDProgressBar(
            color=[0, 0, 0, 1],
            type="determinate",
            running_duration=1,
            catching_duration=1.5,
        )
        self.bar_box = BoxLayout(padding=dp(66), pos=(0, dp(-240)))
        self.bar.start()
        self.bar_box.add_widget(self.bar)
        self.layout.add_widget(self.bar_box)
        self.splash.add_widget(self.layout)
        self.final.add_widget(self.splash)
        self.final.transition = RiseInTransition(duration=1)
        self.final.current = "splash"

        with open("config.json", "r") as file:
            self.config = json.load(file)
        Clock.schedule_once(self.main_load, 5)
        if platform == "android" or self.config["splash"] == 0:
            from main_app import MainScreen

            return MainScreen()
        else:

            Clock.schedule_once(self.load, 2)
            return self.final


Main().run()
