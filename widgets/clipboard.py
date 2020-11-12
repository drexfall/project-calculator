from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.relativelayout import RelativeLayout, FloatLayout
from kivy.uix.button import Button
from kivy.properties import NumericProperty, ListProperty, VariableListProperty, ObjectProperty,StringProperty
from widgets.button import MButton


class ClipButtons(BoxLayout):
    copy_button = ObjectProperty()
    cut_button = ObjectProperty()
    paste_button = ObjectProperty()
    font_size = StringProperty('14dp')
    def on_size(self, *args, **kwargs):
        for button in (self.copy_button, self.cut_button, self.paste_button):
            button.size[1] = self.parent.size[1]*0.1

    def clip_action(self, *args, **kwargs):
        input = self.parent.parent.parent.pages.current_screen.children[0].entry
        data = input.selection_text if input.selection_text else input.text

        if args[0].text == 'Copy':
            input.copy(data)
        elif args[0].text == "Cut":
            input._cut(data)
            if data == input.text:
                input.text = ''
        elif args[0].text == 'Paste':
            input.paste()
        input.delete_selection()

    def __init__(self, *args, **kwargs):

        super(ClipButtons, self).__init__(**kwargs)

        self.copy_button = MButton(text='Copy',
                                   font_size = self.font_size)
        self.cut_button = MButton(text='Cut',
                                   font_size = self.font_size)
        self.paste_button = MButton(text='Paste',
                                   font_size = self.font_size)

        for widget in (self.copy_button, self.cut_button, self.paste_button):
            widget.bind(on_release=self.clip_action)
            self.add_widget(widget)
