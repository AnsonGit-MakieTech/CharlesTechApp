from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.metrics import dp,sp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivymd.uix.gridlayout import MDGridLayout

from login import login_components
  
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView 
from kivy.effects.dampedscroll import DampedScrollEffect
from time import time
import os

from kivy.animation import Animation
  
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.properties import StringProperty
import os

import webbrowser

class Ticket(FloatLayout):
    
    background_image = StringProperty('')
    parent_event : callable = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # ✅ Set the background image path BEFORE adding widgets
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        self.background_image = os.path.join(parent_dir, 'assets', 'ticket_background.png') 

    def on_parent(self, *args):
        Animation(opacity=1, duration=0.5).start(self)
        
    def on_touch_down(self, touch):
        """ ✅ Detect click/tap event and execute action """
        if self.collide_point(*touch.pos):
            print("🎟️ Ticket Clicked!")  # Debugging
            if self.parent_event:
                self.parent_event()
            return True
        return super().on_touch_down(touch)

class CallControl:
    def __init__(self, interval=1):
        self.interval = interval
        self.last_call = 0

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            now = time()
            if now - self.last_call > self.interval:
                self.last_call = now
                func(*args, **kwargs)
        return wrapper


class CustomScrollEffect(DampedScrollEffect):
    
    parent_event : callable = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controlled_callback = self.do_refresh_controlled

    def on_overscroll(self, *args):
        super().on_overscroll(*args)
        if self.overscroll < -50:  # Pulling down
            self.controlled_callback()

    @CallControl(interval=1)
    def do_refresh_controlled(self):
        print("🔄 Pull-to-refresh triggered!")
        self.parent_event()


class CustomScrollView(ScrollView):
    def __init__(self, **kwargs):
        kwargs['effect_cls'] = CustomScrollEffect
        super().__init__(**kwargs)

        self.effect_cls.parent_event = self.on_pull_refresh
        print(kwargs)

    def on_pull_refresh(self):
        print("✅ Custom refresh triggered from CustomScrollView")
        if self.parent:
            self.parent.parent.refresh_callback()
        
class SearchBoxTicket(login_components.LoginTextInput): 
        
    def update_padding(self, *args):
        """ Dynamically center text vertically """
        self.padding_y_dynamic = (self.height - self.line_height) / 2 if self.height > 0 else 8
        print("happen here")
        
class TicketListScreen(Screen):
    
    main_parent : FloatLayout = ObjectProperty(None)
    text_input_font_size = NumericProperty(0)
    search_box : SearchBoxTicket = ObjectProperty(None)
    refresh_layout : CustomScrollView = ObjectProperty(None)
    ticket_list : MDGridLayout = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.update_size)  # Bind window resize event
        
        self.tried = False
    
    def on_enter(self, *args):
        self.search_box.update_padding()
    

    def on_parent(self, *args):
        if self.parent:
            self.main_parent.height = self.parent.height - dp(65)
        # print("on_pre_enter : ", self.main_parent.height)
        # print("args : ", args) 

    def update_size(self, *args):
        """ Update circle size dynamically when window size changes """  
        self.text_input_font_size = min(Window.width, Window.height) * 0.04
        print("update_size : ", self.text_input_font_size)


    def refresh_callback(self, *args): 
        print("happen 2")
        
        # ✅ Create a new ticket
        new_ticket = Ticket()

        # ✅ Insert at the first position
        self.ticket_list.add_widget(new_ticket, index=len(self.ticket_list.children))
        
        # self.open_google_maps(14.5995, 120.9842)
        

    def open_google_maps(self, destination_lat, destination_lon):
        """ Opens Google Maps with directions from current location to a given destination. """
        url = f"https://www.google.com/maps/dir/?api=1&origin=current+location&destination={destination_lat},{destination_lon}"
        webbrowser.open(url)
