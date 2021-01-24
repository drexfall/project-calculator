import json
import os
import sys

from kivy.resources import resource_add_path
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivymd.uix.screen import MDScreen
from kivy.utils import platform, rgba
from kivymd.app import MDApp
from kivymd.uix.progressbar import MDProgressBar
from kivy.uix.image import AsyncImage


class Main(MDApp):
    def resize(self, *args):
        if args[1] < dp(600) or args[2] < dp(600):
            args[0].size = dp(600), dp(600)

    def load(self, *args):
        from main_app import MainScreen

        self.main = MDScreen(name="main")
        self.main.add_widget(MainScreen())
        self.final.add_widget(self.main)
        Window.bind(on_resize=self.resize)

    def main_load(self, *args):

        temp = Window.left + dp(125), Window.top
        if platform != "android" and self.config["splash"] != 0:
            self.final.current = "main"

        def change(dt):
            Animation(
                size=(dp(600), dp(600)),
                left=temp[0],
                duration=0.4,
                t="in_out_cubic",
            ).start(Window)
            Window.borderless = 0

        Clock.schedule_once(change, 0.5)

    def build(self):
        Window.borderless = 1
        self.final = ScreenManager()
        self.splash = MDScreen(name="splash")
        self.splash_image = AsyncImage(
            source="splash.png",
        )
        self.splash.add_widget(self.splash_image)
        self.bar = MDProgressBar(
            color=rgba([250, 206, 173, 255]),
            type="determinate",
            running_duration=2,
            catching_duration=2.5,
        )
        self.bar_box = BoxLayout(padding=dp(98), pos=(0, dp(-245)))
        self.bar.start()
        self.bar_box.add_widget(self.bar)
        self.splash.add_widget(self.bar_box)
        self.final.add_widget(self.splash)
        self.final.transition = SlideTransition(duration=0.5)
        self.final.current = "splash"
        try:
            with open("config.json", "r") as file:
                self.config = json.load(file)
        except FileNotFoundError:
            with open("config.json", "w+") as config:
                json.dump({
                    "base": "e",
                    "open_page": "standard",
                    "history_length": 50,
                    "inverse": 0,
                    "radian": 1,
                    "theme": "Lovely Lavender",
                    "theme_colors": [
                        [
                            "Lovely Lavender",
                            [
                                19,
                                21,
                                22
                            ],
                            [
                                107,
                                127,
                                215
                            ],
                            [
                                241,
                                241,
                                241
                            ],
                            [
                                92,
                                65,
                                93
                            ]
                        ],
                        [
                            "Perfect Peach",
                            [
                                7,
                                6,
                                0,
                                255
                            ],
                            [
                                234,
                                82,
                                111,
                                255
                            ],
                            [
                                247,
                                247,
                                255,
                                255
                            ],
                            [
                                35,
                                181,
                                211,
                                255
                            ]
                        ],
                        [
                            "Magestic Magenta",
                            [
                                28,
                                48,
                                65,
                                255
                            ],
                            [
                                137,
                                4,
                                61,
                                255
                            ],
                            [
                                236,
                                206,
                                142,
                                255
                            ],
                            [
                                178,
                                171,
                                242,
                                255
                            ]
                        ],
                        [
                            "Totally Teal",
                            [
                                255,
                                255,
                                255,
                                255
                            ],
                            [
                                132,
                                220,
                                198,
                                255
                            ],
                            [
                                34,
                                34,
                                34,
                                255
                            ],
                            [
                                75,
                                78,
                                109,
                                255
                            ]
                        ],
                        [
                            "Coffee Cool",
                            [
                                63,
                                13,
                                18,
                                255
                            ],
                            [
                                167,
                                29,
                                49,
                                255
                            ],
                            [
                                241,
                                240,
                                204,
                                255
                            ],
                            [
                                213,
                                191,
                                134,
                                255
                            ]
                        ]
                    ],
                    "splash": 1,
                    "format": "%m/%d/%Y",
                    "page_list": [{
                        "mode": "standard",
                        "row": 6,
                        "col": 5,
                        "text": [
                            " ",
                            "rm",
                            "db",
                            "Del",
                            "AC",
                            "\u00f7",
                            "1",
                            "2",
                            "3",
                            "%",
                            "x",
                            "4",
                            "5",
                            "6",
                            "a\u00b2",
                            "+",
                            "7",
                            "8",
                            "9",
                            "\u221aa",
                            "-",
                            "(",
                            "0",
                            ")",
                            "a!",
                            "...",
                            "rm",
                            ".",
                            "rm",
                            "="
                        ]
                    },
                        {
                        "mode": "scientific",
                        "row": 7,
                        "col": 6,
                        "text": [
                            " ",
                            "rm",
                            "INV",
                            "RAD",
                            "Del",
                            "AC",
                            "sin",
                            "cos",
                            "tan",
                            "cosec",
                            "sec",
                            "cot",
                            "\u00f7",
                            "1",
                            "2",
                            "3",
                            "\u03c0",
                            "log",
                            "x",
                            "4",
                            "5",
                            "6",
                            "e",
                            "a\u00b2",
                            "+",
                            "7",
                            "8",
                            "9",
                            "a!",
                            "ceil",
                            "-",
                            "(",
                            "0",
                            ")",
                            "|a|",
                            "floor",
                            "...",
                            "rm",
                            ".",
                            "%",
                            "rm",
                            "="
                        ],
                        "inv_text": [
                            " ",
                            "rm",
                            "INV",
                            "RAD",
                            "Del",
                            "AC",
                            "sin\u00af\u00b9",
                            "cos\u00af\u00b9",
                            "tan\u00af\u00b9",
                            "cosec\u00af\u00b9",
                            "sec\u00af\u00b9",
                            "cot\u00af\u00b9",
                            "\u00f7",
                            "1",
                            "2",
                            "3",
                            "\u03c0",
                            "log",
                            "x",
                            "4",
                            "5",
                            "6",
                            "e",
                            "\u221aa",
                            "+",
                            "7",
                            "8",
                            "9",
                            "a!",
                            "ceil",
                            "-",
                            "(",
                            "0",
                            ")",
                            "|a|",
                            "floor",
                            "...",
                            "rm",
                            ".",
                            "%",
                            "rm",
                            "="
                        ]
                    },
                        {
                        "mode": "convert",
                        "row": 6,
                        "col": 4,
                        "text": [
                            " ",
                            "rm",
                            " ",
                            "AC",
                            "from",
                            " ",
                            "to",
                            " ",
                            "1",
                            "2",
                            "3",
                            "up",
                            "4",
                            "5",
                            "6",
                            "down",
                            "7",
                            "8",
                            "9",
                            ".",
                            "...",
                            "0",
                            "rm",
                            "="
                        ]
                    },
                        {
                        "mode": "days",
                        "row": 6,
                        "col": 4,
                        "text": [
                            " ",
                            "rm",
                            "between",
                            "rm",
                            "rm",
                            " ",
                            "and",
                            " ",
                            "1",
                            "2",
                            "3",
                            "include up",
                            "4",
                            "5",
                            "6",
                            "include down",
                            "7",
                            "8",
                            "9",
                            "format",
                            "...",
                            "0",
                            "-",
                            "="
                        ]
                    }
                    ]
                }, config, indent=4)
                config.seek(0)
                self.config = json.load(config)
        Clock.schedule_once(self.main_load, 3.5)
        if platform == "android" or self.config["splash"] == 0:
            from main_app import MainScreen

            return MainScreen()
        else:

            Clock.schedule_once(self.load, 2)
            return self.final


if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    Main().run()
