from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineListItem

from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList, OneLineAvatarIconListItem, IconLeftWidget
from kivymd.uix.list import TwoLineAvatarIconListItem, IconLeftWidget, IconRightWidget
from kivy.lang import Builder

from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen

import sqlite3

class DetailScreen(Screen):

    level = ObjectProperty()

    def on_enter(self):
        self.ids.mytitle.title = self.level.get('name')
        print('Detail Screen -----')
        print(self.level)
        print('-----')

class MainScreen(Screen):


    def on_enter(self):

        con = sqlite3.connect('db.sqlite3')
        cur = con.cursor()

        cur.execute('select * from levels')
        levels = cur.fetchall()
        
        self.lst = []

        for x in levels:
            self.lst.append({'id': x[0], 'availebl': x[1], 'name': x[2]})

        print(self.lst)
        for i in self.lst:
            self.ids.box.add_widget(
                TwoLineAvatarIconListItem(
                    IconLeftWidget(icon='circle' if i.get('availebl') == 1 else 'lock'),
                    IconRightWidget(icon='minus'),
                    id=str(i.get('id')),
                    text=i.get('name'),
                    secondary_text='Secondary text here',
                    on_release=self.get_level,
                ),
            )


    def get_level(self, instance):
        MDApp.get_running_app().sm.add_widget(DetailScreen(name='detail_screen'))
        #print(instance.id, instance.text)
        print(instance.text, ' <<')
        DetailScreen.level = {'id': instance.id, 'name': instance.text}
        #DetailScreen.level = instance.text
        self.manager.current = 'detail_screen'




class MyApp(MDApp):
    
    def build(self):
        
        Builder.load_file('main.kv')

        self.sm = ScreenManager()
        self.sm.add_widget(MainScreen(name='main_screen'))

        self.theme_cls.theme_style = "Light"
        return self.sm

    def on_start(self):
        pass


if __name__ == '__main__':
    MyApp().run()

