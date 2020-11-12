from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import (BooleanProperty, ColorProperty, ListProperty,
                             NumericProperty, ObjectProperty, StringProperty)
from kivy.uix.behaviors.touchripple import (TouchRippleBehavior,
                                            TouchRippleButtonBehavior)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button, ButtonBehavior
from kivy.uix.image import Image
from properties import font_color, hover


class MButton(TouchRippleButtonBehavior, Button):
    ripple_duration_in = NumericProperty(1.5)

    ripple_fade_from_alpha = NumericProperty(0.5)

    ripple_fade_to_alpha = NumericProperty(0.5)

    ripple_rad_default = NumericProperty(4)

    ripple_duration_out = NumericProperty(1.5)

    ripple_color = ListProperty([0, 0, 0.8, 0.7])

    toggle_state = BooleanProperty(False)

    state_enable = BooleanProperty(True)

    icon = StringProperty(None)

    icon_size = ObjectProperty((30, 30))

    icon_padding = NumericProperty(10)

    icon_rotation = NumericProperty(0)

    icon_opacity = NumericProperty(1)

    ripple_duration_out = NumericProperty(0.15)

    ripple_duration_in = NumericProperty(0.1)

    bold = BooleanProperty(False)

    hover_image = StringProperty('widgets/hover.png')

    background_normal = StringProperty('widgets/text.png')

    background_disabled_normal = StringProperty('widgets/text.png')

    background_down = StringProperty('widgets/pressed.png')

    color = ColorProperty(font_color)

    hover_color = ColorProperty()

    old_font_size = NumericProperty(9)

    modal_button = BooleanProperty(False)

    def on_disabled(self, instance, value):
        pass

    def on_touch_down(self, touch):
        if self.disabled:
            return False
        collide_point = self.collide_point(touch.x, touch.y)
        if collide_point:
            touch.grab(self)
            self.ripple_show(touch)

            self.dispatch('on_press')
            return True
        return False

    def on_touch_up(self, touch):
        if self.disabled:
            return False
        if touch.grab_current is self:
            touch.ungrab(self)
            self.ripple_fade()

            def defer_release(dt):

                self.dispatch('on_release')
            Clock.schedule_once(defer_release, self.ripple_duration_out)
            return True
        return False

    def mouse_pos(self, window, pos, **kwargs):
        if not hover[0] and not self.modal_button or self.disabled:
            self.background_normal = self.old_image
            self.color = self.color_
            return

        if self.collide_point(*pos):
            self.color = self.hover_color
            self.background_normal = self.hover_image

        else:
            self.color = self.color_
            self.background_normal = self.old_image

    def on_size(self, *args):
        change = (self.size[0]*0.5+self.size[1]*0.5)*self.old_font_size*0.01
        max_size = 20
        self.font_size = min(change, max_size)

    def __init__(self, **kwargs):
        super(MButton, self).__init__(**kwargs)
        self.old_font_size = max(9, self.font_size)
        self.old_image = self.background_normal
        self.color_ = self.color
        self.hover_color = (
            1-self.color[0], 1-self.color[1], 1-self.color[2], self.color[3])
        if self.hover_image:
            Window.bind(mouse_pos=self.mouse_pos)
