from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from widgets.text import Text
from widgets.layout import MyBoxLayout
from buttonstack import ButtonStack
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.clock import Clock
from widgets.label import MLabel
class Page(MyBoxLayout):
    page_name = StringProperty()
    font_size = NumericProperty()
    rows = NumericProperty()
    cols = NumericProperty()
    text_list = ListProperty()
    old_text = StringProperty()
    def focus_entry(self, *args):
        self.entry.insert_text(' ')
        self.entry.text = ''
        self.focus = True
        self.entry.focus = True

    def scroll_focus(self, *args):
        self.textbox.scroll_x = max(0, self.textbox.scroll_x)
        self.textbox.scroll_x = min(1, self.textbox.scroll_x)

    def __init__(self, *args, **kwargs):
        super(Page, self).__init__(**kwargs)
        self.orientation = 'vertical'

        self.textbox = ScrollView(scroll_type=['bars'],
                                  effect_cls='ScrollEffect',
                                  bar_width=15,
                                  do_scroll_y=False,
                                  size_hint_y = 0.3
                                  )
        
        
        self.entry = Text(size_hint=(None, 1),
                          base_direction='rtl',
                          font_size='75dp',
                          unfocus_on_touch=False)
        
        self.preview = MLabel(halign='right',
                              valign = 'bottom',
                              font_size = self.entry.font_size//3,
                              color=self.entry.foreground_color[:3]+[0.8],
                              size_hint_y=0.1,
                              padding_x=10,
                              markup = True,
                              text = "Type something in!")
        self.preview.bind(on_ref_press = lambda object, text: setattr(self.entry,'text',eval(text)))
        self.preview.bind(on_ref_press = lambda object, text: setattr(object,'text',''))
        
        self.layout = ButtonStack(size_hint=(1, 0.5),
                                  spacing=5,
                                  rows=self.rows,
                                  cols=self.cols,
                                  font_size='15dp',
                                  text_list=self.text_list)
        
        self.textbox.add_widget(self.entry)
        Clock.schedule_interval(self.scroll_focus, 0.1)

        self.layout.buttons[0][0].text = self.page_name
        self.layout.size_change(0, 0, 2)
        self.layout.size_change(-1, -1, 2)

        for widget in (self.preview, self.textbox, self.layout):
            self.add_widget(widget)
