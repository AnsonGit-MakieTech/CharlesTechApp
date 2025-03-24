from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.metrics import dp,sp 
from kivy.core.window import Window 
from kivy.uix.button import Button
from kivy.uix.image import Image
from types import MethodType  # ✅ Import MethodType
 
from kivy.animation import Animation
  
from kivy.uix.floatlayout import FloatLayout 
import os
from variables import *
from .home_component import *


class TicketTransactionScreeen(Screen):
     
    main_parent : FloatLayout = ObjectProperty(None)
    text_input_font_size : int = NumericProperty(0)
    title_font_size : int = NumericProperty(0)
    back_image: Image = ObjectProperty(None)
    back_text: Button = ObjectProperty(None)
    go_back_screen_font_size = NumericProperty(0)  # ✅ Initialize with 0 (Will update later)
    go_back_icon : str = StringProperty('')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        parent_dir = os.path.dirname(os.path.dirname(__file__)) 
        
        self.go_back_icon = os.path.join(parent_dir, 'assets', 'go_back_icon.png')
        self.bind(size=self.update_size)  # Bind window resize event
        
    
    def on_parent(self, *args):
        if self.parent:
            self.main_parent.height = self.parent.height - dp(65)
 
    def update_size(self, *args):
        """ Update circle size dynamically when window size changes """  
        self.body_font_size = min(Window.width, Window.height) * 0.04
        self.title_font_size = min(Window.width, Window.height) * 0.05
        self.go_back_screen_font_size = min(Window.width, Window.height) * 0.04
        print("update_size : ", self.text_input_font_size)


    def on_enter(self, *args):
        Animation(opacity=1, duration=0.5).start(self)
        
        self.back_text.on_press=self.go_back
            
        def on_touch_down(image, touch):
            """ Detect touch inside the image """
            if image.collide_point(*touch.pos):
                self.go_back()
                return True  # ✅ Stops event propagation if needed
            return super(image.__class__, image).on_touch_down(touch)  # ✅ Call original method

        # ✅ Bind on_touch_down correctly
        self.back_image.on_touch_down = MethodType(on_touch_down, self.back_image)
        
        return super().on_enter(*args)
    
    def go_back(self, *args): 
        self.manager.transition.duration= 0.5
        self.manager.transition.direction = "right"
        self.manager.current = HOME_SCREEN_TICKETLIST_SCREEN
    
    def on_leave(self, *args):
        Animation(opacity=0, duration=0.5).start(self)
        return super().on_leave(*args)