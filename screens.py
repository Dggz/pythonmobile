from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.properties import ObjectProperty, NumericProperty

import time
import threading


class ScreenOne(Screen):
    pass


class ScreenTwo(Screen):
    health_points = NumericProperty(100)

    def __init__(self, **kwargs):
        super(ScreenTwo, self).__init__(**kwargs)

    def on_health_points(self, instance, value):
        if value < 1:
            self.changeScreen()

    def on_enter(self, *args):
        thread = threading.Thread(target=self.bleed)
        thread.daemon = True
        thread.start()

    def bleed(self, *args):
        while self.health_points > 0:
            self.health_points -= 5
            time.sleep(0.1)

    def displayScreenThenLeave(self):
        self.changeScreen()

    def changeScreen(self):
        if self.manager.current == 'screen1':
            self.manager.current = 'screen2'
        else:
            self.manager.current = 'screen1'


class Manager(ScreenManager):

    screen_one = ObjectProperty(None)
    screen_two = ObjectProperty(None)


class ScreensApp(App):

    def build(self):
        m = Manager(transition=NoTransition())
        return m

if __name__ == "__main__":
    ScreensApp().run()
