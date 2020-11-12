from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.properties import BooleanProperty, ObjectProperty, NumericProperty, StringProperty
from properties import *

class MyBoxLayout(BoxLayout):
    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(1,1,1,1)
            Rectangle(pos=self.pos, size=self.size)