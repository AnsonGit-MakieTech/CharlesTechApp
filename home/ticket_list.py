from kivy.uix.accordion import DictProperty
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
from kivymd.app import MDApp

from variables import *
from .home_component import *

import time
import uuid


class Ticket(FloatLayout):
    
    background_image = StringProperty('')
    parent_event : callable = ObjectProperty(None)
    ticket_number = StringProperty('S234HSFJD')
    ticket_type = StringProperty('Installation')
    ticket_date = StringProperty('Jan 23, 2023') 
    ticket_id = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # ✅ Set the background image path BEFORE adding widgets
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        self.background_image = os.path.join(parent_dir, 'assets', 'ticket_background.png') 
        self.ticket_id = str(uuid.uuid4())

    def on_parent(self, *args):
        Animation(opacity=1, duration=0.5).start(self)
        
    def on_touch_down(self, touch):
        """ ✅ Detect click/tap event and execute action """
        print("Parent event ")
        if self.collide_point(*touch.pos):
            print("🎟️ Ticket Clicked!")  # Debugging
            if self.parent_event:
                print("Ticket id: ", self.ticket_id)
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

    tickets : dict = DictProperty({})
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.update_size)  # Bind window resize event
        
    
    def on_enter(self, *args):
        Animation(opacity=1, duration=0.5).start(self)
        # self.refresh_layout.on_pull_refresh()
        self.search_box.update_padding()

        if len(self.tickets) == 0:
            self.refresh_callback()
        
        transact_screen = self.manager.get_screen(HOME_SCREEN_TRANSACT_SCREEN)
        if transact_screen.has_changed_data:
            self.refresh_callback()
            transact_screen.has_changed_data = False
        
        return super().on_enter(*args)

    def on_pre_leave(self, *args): 
        Animation(opacity=0, duration=0.5).start(self)
        return super().on_leave(*args)

    def on_parent(self, *args):
        if self.parent:
            self.refresh_layout.setup_effect_callback(self.refresh_callback)
            self.main_parent.height = self.parent.height - dp(65)
        # print("on_pre_enter : ", self.main_parent.height)
        # print("args : ", args) 

    def update_size(self, *args):
        """ Update circle size dynamically when window size changes """  
        self.text_input_font_size = min(Window.width, Window.height) * 0.04
        print("update_size : ", self.text_input_font_size)


    def refresh_callback(self, *args): 
        app = MDApp.get_running_app()
        key = "TICKET_LIST"
        if key not in app.communications.key_running:
            app.communications.get_ticket_list()

            def communication_event(*args):
                data = app.communications.get_and_remove(key) 
                print("data : ", data)
                if data.get("result", None):
                    raw_tickets = data.get("data", {})

                    for rkwy, ticket_data in raw_tickets.items():
                        if rkwy in self.tickets:
                            self.tickets[rkwy].update(ticket_data)
                        else:
                            self.tickets[rkwy] = ticket_data

                    # Remove the keys that are not in the raw_tickets dictionary
                    to_remove = [lkey for lkey in self.tickets if lkey not in raw_tickets]
                    for rkey in to_remove:
                        del self.tickets[rkey]



                
                    if len(self.tickets) > 0:
                        self.ticket_list.clear_widgets()
                        
                        for tkey , ticket in self.tickets.items():
                            new_ticket = Ticket()
                            try:
                                new_ticket.ticket_number = ticket.get("ticketnumber", "N/A")
                                new_ticket.ticket_type = ticket.get("tickettype", "N/A")
                                new_ticket.ticket_date = ticket.get("ticket_open_date", "N/A")
                            except Exception as e:
                                print("Error : ", e)
                                new_ticket.ticket_number = "N/A"
                                new_ticket.ticket_type = "N/A"
                                new_ticket.ticket_date = "N/A"

                            new_ticket.parent_event = lambda td=ticket: self.change_screen(td)
                            self.ticket_list.add_widget(new_ticket, index=len(self.ticket_list.children))
                            print("ticket : ", ticket)
                            time.sleep(0.1)
                    return False
                elif data.get("result", False) == False: 
                    return False
                elif data.get("result", False) == None:
                    return False
                    

            Clock.schedule_interval(communication_event, 1)


        # ✅ Create a new ticket
        # new_ticket = Ticket()
        # def open_ticket( ):
        #     print("Ticket Clicked!")  # Debugging
        #     self.change_screen({})
        # new_ticket.parent_event = open_ticket

        # # ✅ Insert at the first position
        # self.ticket_list.add_widget(new_ticket, index=len(self.ticket_list.children))
        
        # self.open_google_maps(14.5995, 120.9842)
    
    def change_screen(self, ticket : dict):
        # print("ticket_index : ", ticket_index)
        transact_screen = self.manager.get_screen(HOME_SCREEN_TRANSACT_SCREEN)
        transact_screen.ticket = ticket
        self.manager.transition.duration= 0.5
        self.manager.transition.direction = "left"
        self.manager.current = HOME_SCREEN_TRANSACT_SCREEN





