
import io
import json

from kivymd.uix.behaviors import elevation
from properties import color,theme_image,config_data,current_page

import qrcode
from kivy.core.clipboard import Clipboard
from kivy.core.image import Image as CoreImage
from kivy.properties import ListProperty, ObjectProperty, StringProperty,NumericProperty
from kivy.uix.image import Image
from kivy.uix.modalview import ModalView
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import (CheckboxLeftWidget, MDList)
from kivymd.uix.toolbar import MDToolbar
from kivy.metrics import dp
from widgets import Container, Icon, ListItem, MyBoxLayout
from kivy.uix.recycleview import RecycleView



class History(MyBoxLayout):

    to_delete = False
    left_check_list = ListProperty()
    main = ObjectProperty()
    def item_check(self, *args):
        count = 0
        def checkall(*args):
            count = 0
            for item in self.left_check_list:
                item.state = 'down'
                count+=1
            
            self.toolbar.left_action_items = [["select-all", uncheckall]]
            self.toolbar.right_action_items = [["delete-sweep", self.action]]
            
        def uncheckall(*args):
            for item in self.left_check_list:
                item.state = 'normal'
            self.toolbar.left_action_items = self.toolbar.right_action_items = []
            
        
        for item in self.left_check_list:
            if item.state == 'down':
                count += 1
        
        if count>0 and args[0].text!='yes':
            self.toolbar.left_action_items = [["select", checkall]] if count==1 else [["select-all", uncheckall]]
            self.toolbar.right_action_items = [["delete", self.action]] if count==1 else [["delete-sweep", self.action]]
        else:
            uncheckall()
            
    def refresh(self, *args):
        self.layout.clear_widgets()
        self.left_check_list = []
        with open('history.json', 'r+') as data:
            data = json.load(data)
            for list_data in data:
                list_container = Container()
                list_item = ListItem(text=str(list(data[list_data][0].keys())[0]+' = '+list(data[list_data][0].values())[0]),
                                     secondary_text=data[list_data][1],
                                     time=list_data,
                                     container=list_container,
                                     width_mult = 1.4)

                left_check = CheckboxLeftWidget()
                left_check.unselected_color = list_item.text_color
                left_check.update_color()
                left_check.update_primary_color(self,list_item.text_color)
                left_check.bind(on_release=self.item_check)
                list_item.add_widget(left_check)
                self.left_check_list.append(left_check)

                for list_container_item in ('content-copy', 'qrcode', 'history'):

                    item = Icon(icon=list_container_item)
                    item.bind(on_release=self.action)
                    list_container.add_widget(item)

                list_item.bind(on_size=lambda arg: print(arg))
                list_item.add_widget(list_container)
                self.layout.add_widget(list_item)
            self.layout.children.reverse()
    def action(self, button):
        
        item = []
        
        if type(button.parent.parent.parent).__name__ == 'History':
            for data in self.left_check_list:
                
                if data.state == 'down':
                    item.append(data.parent.parent)
        else:
            item.append(button.parent.parent.parent)
            item_data = str(item[0].text+' '+item[0].secondary_text)
            
        if button.icon == 'content-copy':
            Clipboard.copy(item_data)

        elif button.icon == 'history':
            self.main.pages.pages_list[current_page[0]].entry.text = item_data.split()[0]
            self.parent.dismiss()
        elif button.icon == 'qrcode':

            image = Image(source="")
            imgIO = io.BytesIO()

            qrcode.make(item_data).save(imgIO, ext='png')

            imgIO.seek(0)
            imgData = io.BytesIO(imgIO.read())
            image.texture = CoreImage(imgData, ext='png').texture
            image.reload()

            dialog = ModalView(size_hint=(None, None),
                               size=image.texture.size)
            dialog.add_widget(image)
            dialog.open()

        elif button.icon in ['delete','delete-sweep']:
            dialog_yes = MDFlatButton(text="yes")
            dialog_no = MDRaisedButton(text="no")
            dialog = MDDialog(text="Delete {} item{}?".format(len(item),'' if len(item)==1 else 's'),
                                buttons=[dialog_no, dialog_yes])

            with open('history.json', 'r') as file:
                data = json.load(file)
                for item_ in item:
                    data.pop(item_.time)
                dialog_no.bind(on_release=dialog.dismiss)
                dialog_yes.bind(on_release=dialog.dismiss)
                dialog_yes.bind(on_release=lambda button: json.dump(
                    data, open('history.json', 'w'), indent=4))
                dialog_yes.bind(on_release=self.item_check)
            dialog.bind(on_dismiss=self.refresh)
            dialog.open()
            

    def __init__(self, **kwargs):
        super(History, self).__init__(**kwargs)
        self.orientation = 'vertical'

        self.toolbar = MDToolbar(title='History',
                                 anchor_title='center',
                                 elevation = 10)
        self.toolbar.md_bg_color = color(f"images/{theme_image[config_data['theme']][2]}.png")
        self.toolbar.specific_text_color = color(f"images/{theme_image[config_data['theme']][0]}.png")
        self.scroll = RecycleView()
        self.layout = MDList()
        self.do_scroll_x = False

        self.refresh()
        self.scroll.add_widget(self.layout)
        self.add_widget(self.toolbar)
        self.add_widget(self.scroll)


if __name__ == "__main__":
    class Main(MDApp):
        def build(self):
            return History()
    Main().run()
