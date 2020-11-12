
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.dropdown import DropDown
from kivy.graphics import Color, Rectangle
from kivy.properties import ColorProperty,ObjectProperty,ListProperty,NumericProperty,BooleanProperty
from kivy.uix.spinner import Spinner,SpinnerOption


        
class PGrid(GridLayout):
    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0,0,0,1)
            Rectangle(pos=self.pos, size=self.size)
            
class PLabel(Label):
    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.95,0.95,0.95,1)
            Rectangle(pos=self.pos, size=self.size)
    color = ColorProperty([0,0,0,1])

class PTextInput(TextInput):
    background_active = 'text.png'
    background_normal = 'text.png'
    background_disabled_normal = 'text.png'
    
    cursor_width = 2
    cursor_color = (0,0,0,1)
    multiline = False
    unfocus_on_touch=False
    
class PStack(StackLayout):
    background_color = (0,0,0,1) 
    
    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.background_color)
            Rectangle(pos=self.pos, size=self.size)
           
class PBox(BoxLayout):
    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.background_color)
            Rectangle(pos=self.pos, size=self.size)
    background_color = (0,0,0,1)        
class PButton(Button):
    background_normal = 'text.png'
    background_down = 'pressed.png'
    background_disabled_normal = 'text.png'
    color = [0,0,0,1]

class PSpinnerButton(SpinnerOption):
    background_normal = 'text.png'
    background_disabled_normal = 'text.png'
    background_down = 'text.png'
    color = [0,0,0,1]

class PSpinner(Spinner):
    background_normal = 'text.png'
    background_down = 'pressed.png'
    background_disabled_normal = 'text.png'
    option_cls = PSpinnerButton
    color = [0,0,0,1]