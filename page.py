from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout

from properties import (
    config_data,
    convert_quantities,
    convert_unit_area,
    convert_unit_currency,
    convert_unit_energy,
    convert_unit_length,
    convert_unit_speed,
    convert_unit_temperature,
    convert_unit_time,
    convert_unit_weight,
    current_page,
)
from widgets import Drop, MButton, MLabel, MyBoxLayout, Text


class ButtonStack(MyBoxLayout):
    rows = NumericProperty(1)
    cols = NumericProperty(1)
    buttons = ListProperty()
    font_size = NumericProperty()
    text_list = ListProperty()

    def drop_close(self, button):
        self.parent.parent.parent.parent.parent.options_close(button)
        if button == self.quantity_drop:
            self.buttons[0][1].text = self.parent.entry.quantity = button.value
            self.from_drop.values = self.to_drop.values = eval(
                "convert_unit_" + button.value
            )
            self.from_drop.refresh()
            self.to_drop.refresh()
            self.buttons[1][1].text = self.from_drop.values[0]
            self.buttons[1][3].text = self.to_drop.values[1]
        elif button == self.from_drop:
            self.buttons[1][1].text = self.parent.entry.from_unit = button.value
        elif button == self.to_drop:
            self.buttons[1][3].text = self.parent.entry.to_unit = button.value

    def size_change(self, row, column, new):
        self.buttons[row][column].parent.size_hint_x *= new

    def options_select(self, button, *args, **kwargs):
        global current_page
        self.options.dismiss()
        current_page[0] = button.text
        self.parent.parent.parent.page_change(button)
    def inverse_change(self, button):
        
        if button.state == 'down':
            text=config_data['page_list'][1]['inv_text']
        else:
            text = config_data['page_list'][1]['text']
        
        c=1    
        for index,row in enumerate(self.buttons):
            for index_,cell in enumerate(row):
                if (index==0 and index_==0) or index>3:
                    c+=1
                    continue
                elif cell.text == 'log' and text == config_data['page_list'][1]['inv_text']:
                    cell.text = str(config_data['base'])+'\u00aa'
                    c+=1
                    continue
                cell.text = text[c] if text[c] not in ['rm',' '] else text[c+1]
                c+=1
    def __init__(self, **kwargs):
        super(ButtonStack, self).__init__(**kwargs)
        self.stack = StackLayout()
        text_var = 0

        for row in range(self.rows):
            row_list = []
            for cell in range(self.cols):

                padding = [self.spacing * 0.5] * 4
                if row == 0:
                    padding[1] = 0
                if row == self.rows - 1:
                    padding[3] = 0
                if cell == 0:
                    padding[0] = 0
                if cell == self.cols - 1:
                    padding[2] = 0

                button_box = BoxLayout(
                    size_hint_x=1 / self.cols,
                    size_hint_y=1 / self.rows,
                    padding=padding,
                )
                button = MButton(
                    font_size=self.font_size, text=self.text_list[text_var]
                )
                text_var += 1
                if button.text == "rm":
                    continue
                button_box.add_widget(button)
                self.stack.add_widget(button_box)
                row_list.append(button)

            self.buttons.append(row_list)

        for index_, button_ in enumerate(self.buttons):
            for index, button in enumerate(button_):
                if button.text == "db":
                    button.disabled = True
                    button.text = ""
                elif button.text in ["and", "between"]:
                    button.hover = False
                    button.ripple = False
                elif "include" in button.text:
                    button.toggle_state = True
                elif button.text in ["INV", "RAD"]:
                    button.toggle_state = True
                    if (config_data["inverse"] and button.text == "INV") or (
                        config_data["radian"] and button.text == "RAD"
                    ):
                        button.state = "down"
                        button.color = button.hover_color
                    if button.text == 'RAD':
                            button.text = 'RAD' if config_data['radian'] else 'DEG'
                            button.bind(on_release = lambda button: setattr(button,'text','RAD' if button.text == 'DEG' else 'DEG'))
                    if button.text == 'INV':
                            button.bind(on_release = self.inverse_change)
                else:
                    if button.text not in [" ", "..."]:
                        button.bind(
                            on_release=lambda button=button: self.parent.entry.insert_text(
                                button.text
                            )
                        )

        self.options = ModalView(size_hint=(0.4, 0.6))
        self.options_layout = MyBoxLayout(orientation="vertical")
        for options_button_text in config_data["page_list"]:
            if options_button_text["mode"] != current_page:
                options_button = MButton(
                    text=options_button_text["mode"], modal_button=True
                )
                self.options_layout.add_widget(options_button)
                options_button.bind(
                    on_release=lambda options_button=options_button: self.options_select(
                        options_button
                    )
                )
        self.options.add_widget(self.options_layout)
        self.options.bind(
            on_dismiss=lambda button: self.parent.parent.parent.parent.parent.options_close(
                button
            )
        )

        self.buttons[0][0].bind(on_release=self.options.open)
        self.buttons[0][0].bind(
            on_release=lambda button: self.parent.parent.parent.parent.parent.options_open(
                button
            )
        )

        self.buttons[-1][0].bind(
            on_release=lambda button: self.parent.parent.parent.parent.parent.effect_layout.settings.open()
        )
        self.buttons[-1][0].bind(
            on_release=lambda button: self.parent.parent.parent.parent.parent.options_open(
                button
            )
        )
        self.spacing = 0

        self.quantity_drop = Drop(
            title="quantity", values=convert_quantities, size_hint=(0.6, 0.6)
        )
        self.from_drop = Drop(
            title="from",
            values=eval("convert_unit_" + convert_quantities[0]),
            size_hint=(0.6, 0.6),
        )

        self.to_drop = Drop(
            title="to",
            values=eval("convert_unit_" + convert_quantities[0]),
            default = eval("convert_unit_" + convert_quantities[0])[1],
            size_hint=(0.6, 0.6)
        )
        
        self.quantity_drop.bind(on_dismiss=lambda button: self.drop_close(button))

        self.from_drop.bind(on_dismiss=lambda button: self.drop_close(button))
        self.to_drop.bind(on_dismiss=lambda button: self.drop_close(button))
        self.add_widget(self.stack)


class Page(MyBoxLayout):
    page_name = StringProperty()
    font_size = NumericProperty()
    rows = NumericProperty()
    cols = NumericProperty()
    text_list = ListProperty()
    old_text = StringProperty()
    preview_text = StringProperty("Type something in here!")

    def focus_entry(self, *args):
        self.entry.insert_text(" ")
        self.entry.text = ""
        self.focus = True
        self.entry.focus = True

    def scroll_focus(self, *args):
        self.text_container.scroll_x = max(0, self.text_container.scroll_x)
        self.text_container.scroll_x = min(1, self.text_container.scroll_x)

    def __init__(self, *args, **kwargs):
        super(Page, self).__init__(**kwargs)
        self.orientation = "vertical"

        self.textbox = MyBoxLayout(padding=[dp(10), 0], size_hint_y=0.3)
        self.text_container = ScrollView(
            scroll_type=["bars"],
            effect_cls="ScrollEffect",
            bar_width=15,
            do_scroll_y=False,
        )

        self.entry = Text(
            size_hint=(None, 1),
            base_direction="rtl",
            font_size="75dp",
            unfocus_on_touch=False,
        )

        self.preview = MLabel(
            halign="right",
            valign="bottom",
            font_size=self.entry.font_size // 3,
            color=self.entry.foreground_color[:3] + [0.8],
            size_hint_y=0.1,
            padding_x=10,
            markup=True,
            text=self.preview_text,
        )
        self.preview.bind(
            on_ref_press=lambda object, text: setattr(self.entry, "text", eval(text))
        )
        self.preview.bind(on_ref_press=lambda object, text: setattr(object, "text", ""))

        self.layout = ButtonStack(
            size_hint=(1, 0.5),
            spacing=5,
            rows=self.rows,
            cols=self.cols,
            font_size=dp(19),
            text_list=self.text_list,
        )

        self.text_container.add_widget(self.entry)
        self.textbox.add_widget(self.text_container)
        Clock.schedule_interval(self.scroll_focus, 0.1)

        self.layout.buttons[0][0].text = self.page_name
        self.layout.size_change(0, 0, 2)
        self.layout.size_change(-1, -1, 2)
        self.spacing = 5
        for widget in (self.preview, self.textbox, self.layout):
            self.add_widget(widget)
