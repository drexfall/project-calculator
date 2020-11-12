
import solve
from kivy.properties import BooleanProperty, NumericProperty
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from properties import config_data, current_page, write_history


class Text(TextInput):

    background_active = 'hover.png'
    background_normal = 'hover.png'
    background_disabled_normal = 'text.png'
    minimum_width = NumericProperty(1)
    cursor_width = 2
    cursor_color = (0, 0, 0, 1)
    write_tab = False

    def on_cursor(self, instance, newPos):
        self.width = max(self.minimum_width, self.parent.width)

        if not (isinstance(self.parent, ScrollView) and self.multiline):
            return super(Text, self).on_cursor(instance, newPos)
        if newPos[0] == 0:
            self.parent.scroll_x = 0
        else:
            over_width = self.width - self.parent.width
            if over_width <= 0.0:
                return super(Text, self).on_cursor(instance, newPos)
            view_start = over_width * self.parent.scroll_x
            view_end = view_start + self.parent.width
            offset = self.cursor_offset()
            desired_view_start = offset - 5
            desired_view_end = offset + \
                self.padding[0] + self.padding[2] + self.cursor_width + 5
            if desired_view_start < view_start:
                self.parent.scroll_x = max(0, desired_view_start / over_width)
            elif desired_view_end > view_end:
                self.parent.scroll_x = min(
                    1, (desired_view_end - self.parent.width) / over_width)
        return super(Text, self).on_cursor(instance, newPos)

    def insert_text(self, substring, from_undo=False):

        if substring in ['\r', '\n', '=']:

            for opr in ['+', '-', '/', '*']:
                if self.text.count(opr):
                    break
            else:
                return

            self.parent.parent.old_text = self.text
            self.parent.parent.preview.text = '[ref=self.old_text]' + \
                self.text+'[/ref]'

            if current_page[0] == 'standard':
                substring = solve.Basic(
                    self.text, config_data['radian'], config_data['base'])
            write_history(self.text, substring, current_page[0])
            self.text = ''

        for sub_ in substring:
            return super(Text, self).insert_text(substring, from_undo=from_undo)

    def on_text(self, instance, newText):

        width_calc = 0
        for line_label in self._lines_labels:
            width_calc = max(width_calc, line_label.width + 90)
        self.minimum_width = width_calc

    def keyboard_on_key_up(self, window, keycode):

        if (keycode[1] == 'right' or keycode[1] == 'left'):
            self.calc_scroll(keycode[1], True)

        key, key_str = keycode
        k = self.interesting_keys.get(key)
        if k:
            key = (None, None, k, 1)
            self._key_up(key)

    def calc_scroll(self, direction, key=None):

        if not key:
            self.do_cursor_movement('cursor_'+direction)

        if direction == 'left':
            limit = '>0'
            sensitivity = '-'
        else:
            limit = '<1'
            sensitivity = '+'

        if eval('self.parent.scroll_x'+limit):
            self.parent.scroll_x += eval(sensitivity+'0.07')
        else:
            self.parent.scroll_x = limit[1:]

        if self.cursor_col == len(self.text):
            self.parent.scroll_x = 1
