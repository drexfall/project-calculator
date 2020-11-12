import csv

from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty, VariableListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.uix.stacklayout import StackLayout

from properties import config_data, current_page
from widgets.button import MButton
from widgets.layout import MyBoxLayout


class ButtonStack(MyBoxLayout):
    rows = NumericProperty(1)
    cols = NumericProperty(1)
    buttons = ListProperty()
    font_size = NumericProperty()
    text_list = ListProperty()

    def size_change(self, row, column, new):
        self.buttons[row][column].parent.size_hint_x *= new
        #next_button = self.buttons[row][column+1 if column == 0 else column-1]
        
        
    def options_select(self, button, *args, **kwargs):
        global current_page
        self.options.dismiss()
        current_page[0] = button.text
        self.parent.parent.parent.page_change(button)

    def __init__(self, **kwargs):
        super(ButtonStack, self).__init__(**kwargs)
        self.stack = StackLayout()
        text_var = 0

        for row in range(self.rows):
            row_list = []
            for cell in range(self.cols):

                padding = [self.spacing*0.5]*4
                if row == 0:
                    padding[1] = 0
                if row == self.rows-1:
                    padding[3] = 0
                if cell == 0:
                    padding[0] = 0
                if cell == self.cols-1:
                    padding[2] = 0

                button_box = BoxLayout(size_hint_x=1/self.cols,
                                       size_hint_y=1/self.rows,
                                       padding=padding)
                button = MButton(font_size=self.font_size,
                                 text=self.text_list[text_var])
                text_var += 1
                if button.text=='rm':
                    continue
                button_box.add_widget(button)
                self.stack.add_widget(button_box)
                row_list.append(button)

            self.buttons.append(row_list)

        for index_,button_ in enumerate(self.buttons):
            for index,button in enumerate(button_):
                if button.text == 'db':
                    button.disabled = True
                    button.text = ''
                else:
                    if button.text not in  [' ','...']:
                        button.bind(on_release = lambda button=button:self.parent.entry.insert_text(button.text))

        self.options = ModalView(size_hint=(0.3, 0.5))
        self.options_layout = MyBoxLayout(orientation='vertical')
        for options_button_text in config_data['page_list']:
            if options_button_text['mode'] != current_page:
                options_button = MButton(text=options_button_text['mode'],
                                         modal_button=True)
                self.options_layout.add_widget(options_button)
                options_button.bind(
                    on_release=lambda options_button=options_button: self.options_select(options_button))
        self.options.add_widget(self.options_layout)
        self.options.bind(
            on_dismiss=lambda button: self.parent.parent.parent.parent.parent.options_close(button))

        self.buttons[0][0].bind(on_release=self.options.open)
        self.buttons[0][0].bind(
            on_release=lambda button: self.parent.parent.parent.parent.parent.options_open(button))

        self.buttons[-1][0].bind(
            on_release=lambda button: self.parent.parent.parent.parent.parent.effect_layout.settings.open())
        self.buttons[-1][0].bind(
            on_release=lambda button: self.parent.parent.parent.parent.parent.options_open(button))
        self.spacing = 0
        self.add_widget(self.stack)
