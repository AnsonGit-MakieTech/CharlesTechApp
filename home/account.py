

from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
import os
from kivy.animation import Animation


class AccountScreen(Screen):

    no_image_path : str = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        self.no_image_path = os.path.join(parent_dir, 'assets', 'profile_no_image.png')

          

    
    def on_leave(self, *args):
        Animation(opacity=0, duration=0.5).start(self)
        return super().on_leave(*args)
    
    def on_enter(self, *args):
        Animation(opacity=1, duration=0.5).start(self)  
        return super().on_enter(*args)





