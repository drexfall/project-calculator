import json
import webbrowser

from kivy.clock import Clock
from kivy.properties import (ListProperty, NumericProperty, ObjectProperty,
                             StringProperty)
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivymd.app import MDApp
from kivymd.uix.selectioncontrol import MDCheckbox, MDSwitch

from properties import config_data
from widgets.button import MButton
from widgets.label import MLabel
from widgets.layout import MyBoxLayout
from kivy.uix.image import Image

class SwitchText(BoxLayout):
    option = ObjectProperty(MDCheckbox)

    def __init__(self, **kwargs):
        super(SwitchText, self).__init__(**kwargs)
        self.text = Label(color=[0, 0, 0, 1])
        self.button_box = BoxLayout()
        self.setting_button = self.option(size_hint=(None, None),
                                          size=(45, 45),
                                          pos_hint={'center_x': 0.5,
                                                    'center_y': 0.5})
        self.add_widget(self.text)
        self.button_box.add_widget(self.setting_button)
        self.add_widget(self.button_box)


class SaveButtons(MyBoxLayout):
    def apply_func(self, *args, **kwargs):
        for x in self.parent.accordion.children:
            if type(x.box).__name__ == 'General':
                global config_data
                config_data.update(x.box.selected)

    def save_func(self, *args, **kwargs):
        self.apply_func()
        with open('config.json', 'r+') as config_file:
            for x in self.parent.accordion.children:
                if type(x.box).__name__ == 'General':
                    data = json.load(config_file)
                    data.update(x.box.selected)
                    config_file.seek(0)
                    config_file.truncate(0)
                    json.dump(data, config_file, indent=4)

    def __init__(self, **kwargs):
        super(SaveButtons, self).__init__(**kwargs)
        self.apply_button = MButton(text='Apply',
                                    modal_button=True)
        self.apply_button.bind(on_release=self.apply_func)
        self.save_button = MButton(text='Save',
                                   modal_button=True)
        self.save_button.bind(on_release=self.save_func)
        self.add_widget(self.apply_button)
        self.add_widget(self.save_button)


class SettingsRow(MyBoxLayout):
    title = StringProperty()
    option = ObjectProperty(SwitchText)
    option_text = ListProperty([''])
    options_list = ListProperty()
    option_name = StringProperty()
    default = StringProperty()

    def touch(self, button):
        for but in self.options_list:
            if but != button:
                but.active = False
                button.active = True
        if button.parent.parent.text.text:
            self.parent.selected[self.option_name] = button.parent.parent.text.text
        else:
            self.parent.selected[self.option_name] = 1 if button.state == 'down' else 0

    def __init__(self,  **kwargs):
        super(SettingsRow, self).__init__(**kwargs)
        self.padding = [20, 0, 20, 0]
        self.title_option = Label(halign='left',
                                  valign='middle',
                                  text=self.title,
                                  color=[0, 0, 0, 1])
        self.title_option.bind(size=self.title_option.setter('text_size'))
        self.add_widget(self.title_option)
        for opt_text in self.option_text:
            self.setting_option = self.option(size_hint_x=0.2,
                                              pos_hint={'right': 0})
            self.setting_option.text.text = opt_text
            self.setting_option.setting_button.bind(on_release=self.touch)
            self.options_list.append(self.setting_option.setting_button)
            if self.setting_option.text.text == self.default or self.default == '1':
                self.setting_option.setting_button.state = 'down'
            self.add_widget(self.setting_option)


class General(MyBoxLayout):
    selected = {'base': config_data['base'],
                'inverse': config_data['inverse'],
                'radian': config_data['radian']}

    def __init__(self, **kwargs):
        super(General, self).__init__(**kwargs)
        for index, option_tuple in enumerate(((['e', '10', '2'], 'Base for logarithm'),
                                              ([''], 'Inverse on start'),
                                              ([''], 'Radian on start'))):

            self.base_set = SettingsRow(size_hint_y=0.1,
                                        title=option_tuple[1],
                                        option_text=option_tuple[0],
                                        option_name=list(self.selected.keys())[
                                            index],
                                        default=str(list(self.selected.values())[index]))
            self.add_widget(self.base_set)

        self.add_widget(MyBoxLayout(size_hint_y=0.3))


class Themes(MyBoxLayout):
    def __init__(self, **kwargs):
        super(Themes, self).__init__(**kwargs)


class About(MyBoxLayout):
    color = [0, 0, 0, 1]

    def __init__(self, **kwargs):
        super(About, self).__init__(**kwargs)
        self.padding = [75, 30]
        self.header = MLabel(text='Calculator',
                             valign='top',
                             bold=True,
                             font_size = '25dp',
                             size_hint_y = 0.6)
        self.body1 = MLabel(text='This project was made keeping the power of Python and flexibillity of open source software in mind.',
                            font_size = '18dp',
                           valign='top')
        self.logo = Image()
        self.footer = MyBoxLayout()
        self.footer.source_code = MLabel(text='[ref=https://www.github.com]source code here[/ref]',
                            font_size = '15dp',
                           valign='bottom',
                           halign = 'left',
                           markup=True,
                           size_hint = (0.5,1))
        self.footer.credits = MLabel(text='Aman Singh (XII-E)\nShreyash Singh (XII-D)\nVineet Pratap Singh (XII-D)',
                            font_size = '15dp',
                            halign = 'right',
                           valign='bottom',
                           size_hint = (0.5,1))
        self.footer.add_widget(self.footer.source_code)
        self.footer.add_widget(self.footer.credits)
        
        self.footer.source_code.bind(on_ref_press = lambda args,args1: webbrowser.get().open_new_tab(args1))
        for widget_key in [text for text in self.__dict__ if not text.startswith('_') and not text == 'canvas']:
            widget = self.__dict__[widget_key]
            self.add_widget(widget)


class Settings(MyBoxLayout):

    def __init__(self, *args, **kwargs):
        super(Settings, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.accordion = Accordion(orientation='vertical')
        for x in [General, Themes, About]:
            item = AccordionItem(title=str(x.__name__))
            item.box = x(orientation='vertical')
            item.add_widget(item.box)
            self.accordion.add_widget(item)

        for x in self.accordion.children:
            x.collapse = False if type(x.box).__name__ == 'General' else True

        self.add_widget(self.accordion)
        self.save_buttons = SaveButtons(size_hint_y=0.1)
        self.add_widget(self.save_buttons)


class Main(MDApp):
    def build(self):
        return Settings()


if __name__ == '__main__':
    Main().run()
