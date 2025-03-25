from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.metrics import dp,sp 
from kivy.core.window import Window
from kivymd.uix.gridlayout import MDGridLayout

from login import login_components
   
from kivy.animation import Animation
  
from kivy.uix.floatlayout import FloatLayout 
from kivy.properties import StringProperty
import os


from variables import *
from .home_component import *


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
        Animation(opacity=1, duration=0.5).start(self)
        self.refresh_layout.setup_effect_callback(self.refresh_callback)
        # self.refresh_layout.on_pull_refresh()
        self.search_box.update_padding()
    
    def on_pre_leave(self, *args):
        Animation(opacity=0, duration=0.5).start(self)
        return super().on_leave(*args)

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
        def open_ticket( ):
            print("Ticket Clicked!")  # Debugging
            self.change_screen('ticket_id')
        new_ticket.parent_event = open_ticket

        # ✅ Insert at the first position
        self.ticket_list.add_widget(new_ticket, index=len(self.ticket_list.children))
        
        # self.open_google_maps(14.5995, 120.9842)
    
    def change_screen(self, ticket_id : str):
        self.manager.transition.duration= 0.5
        self.manager.transition.direction = "left"
        self.manager.current = HOME_SCREEN_TRANSACT_SCREEN





