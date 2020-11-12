from widgets.button import MButton
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.effectwidget import (EffectWidget, HorizontalBlurEffect,
                                   VerticalBlurEffect)

from kivy.uix.modalview import ModalView
from kivy.uix.screenmanager import Screen, ScreenManager, WipeTransition
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog

from buttonstack import ButtonStack
from page import Page
from properties import (button_text_scientific, button_text_standard,
                        config_data, current_page, hover,platform)
from settings import Settings
from widgets.clipboard import ClipButtons
from widgets.layout import MyBoxLayout
from widgets.text import Text
from kivymd.uix.picker import MDDatePicker
if platform != 'android':
    def size(dt):
        Window.minimum_width, Window.minimum_height = (400, 700)
    Clock.schedule_once(size,1)
    
class Pages(ScreenManager):
    pages_list = {}
    def page_change(self, button, *args, **kwargs):
        self.current = button.text
        self.pages_list[self.current].focus_entry()
    def __init__(self, *args, **kwargs):
        super(Pages, self).__init__(**kwargs)

        self.transition = WipeTransition(duration=0.5)

        for page_list in (config_data['page_list']):
            self.page_screen = Screen(name=page_list["mode"])
            self.page = Page(page_name=page_list["mode"],
                             rows=page_list["row"],
                             cols=page_list["col"],
                             text_list=page_list["text"])

            if page_list["mode"] == 'days':
                self.page.layout.size_change(0,1,2)
                self.page.layout.size_change(1,0,1.5)
                self.page.layout.size_change(1,2,1.5)
                self.page.layout.size_change(-1,-1,0.5)
                
                
                
            elif page_list["mode"] == 'convert':
                self.page.layout.size_change(0,1,2)
                
                
                
            elif page_list["mode"] == 'standard':
                self.page.layout.size_change(-1,0,2)

            self.page_screen.add_widget(self.page)
            self.add_widget(self.page_screen)
            self.pages_list.update({page_list['mode']:self.page})
        
        Clock.schedule_once(self.pages_list[config_data['page_list'][0]['mode']].focus_entry,2)

class MainScreen(EffectWidget):
    def options_open(self, button, *args, **kwargs):
        global hover

        button.background_normal = button.old_image
        self.effects = [HorizontalBlurEffect(size=5),
                        VerticalBlurEffect(size=5)]
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
        top = (input.parent.size[1]//3)-input.parent.parent.preview.size[1]//2
        input.padding = [0, top]

    def __init__(self, *args, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        self.effect_layout = MyBoxLayout(orientation='vertical',
                                         padding = 5)
        self.header_buttons = MyBoxLayout(size_hint_y = 0.1)
        self.header_buttons.add_widget(ClipButtons(spacing=5,
                                                  size_hint_x = 0.3,
                                                  font_size='20dp'))
        self.header_buttons.add_widget(MyBoxLayout())
        self.header_buttons.add_widget(MButton(size_hint_x = 0.1))
        self.pages = Pages(size_hint=(1, 0.9))
        
        self.effect_layout.add_widget(self.header_buttons)
        self.effect_layout.add_widget(self.pages)
        
        self.add_widget(self.effect_layout)

        self.effect_layout.settings = ModalView(size_hint=(0.8, 0.9))
        self.settings_page = Settings(padding=5,
                                      spacing=5)
        self.settings_page.save_buttons.save_button.bind(
            on_release=self.effect_layout.settings.dismiss)
        self.effect_layout.settings.add_widget(self.settings_page)
        self.effect_layout.settings.bind(on_dismiss=self.options_close)

        Clock.schedule_interval(self.text_halign, 0.1)


class Main(MDApp):
    def build(self):
        return MainScreen()


if __name__ == "__main__":
    Main().run()
