from kivy.uix.label import Label
from kivy.properties import StringProperty,NumericProperty,ColorProperty,ListProperty
from kivy.core.window import Window
class MLabel(Label):
    color = ColorProperty([0,0,0,1])
    halign = StringProperty('center')
    valign = StringProperty('center')

    def __init__(self, *args, **kwargs):
        super(MLabel,self).__init__(**kwargs)

        self.bind(size=self.setter('text_size'))
