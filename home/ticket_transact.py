from kivy.uix.accordion import ListProperty
from kivy.uix.accordion import BooleanProperty
from kivy.uix.accordion import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, NumericProperty, StringProperty , BooleanProperty, ListProperty
from kivy.metrics import dp,sp 
from kivy.core.window import Window 
from kivy.uix.button import Button
from kivy.uix.image import Image
from types import MethodType  # ✅ Import MethodType
 
from kivy.animation import Animation
  
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout 
import os
from variables import *
from .home_component import *

import webbrowser
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.modalview import ModalView
from kivy.uix.scrollview import ScrollView





class GeolocationStepLayout(MDBoxLayout):
    is_not_done : bool = BooleanProperty(True)
    step_text : str = StringProperty('Step 3: Geo-Mapping Submission')

class Step1Layout(MDBoxLayout):
    old_account : bool = BooleanProperty(False)
    is_not_done : bool = BooleanProperty(True)




class Remark(BoxLayout):
    remark_text : str = StringProperty('This is a remark')


class RemarksListViewer(ModalView):
    pass
     

class RemarksInputLayout(ModalView):
    remark_text : TextInput = ObjectProperty(None)
    is_ready_to_submit : bool = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.remark_text.bind(text=self.on_text_change)
    
    def on_open(self):
        self.remark_text.focus = True
    
    def on_text_change(self, instance, value):
        self.is_ready_to_submit = len(value) > 0
    


class AccountInfoLayout(MDBoxLayout):
    icon_image : str = StringProperty('')
    account_info : str = StringProperty("......")
    click_event : object = ObjectProperty(None)
    
    info_label : BoxLayout = ObjectProperty(None)
    
    def setup(self, icon_image = None, account_info = None , click_event = None):
        if (icon_image):
            self.icon_image = icon_image
        if (account_info): 
            
            if (click_event):  
                def on_touch_down(label, touch):
                    """ Detect touch inside the image """
                    if label.collide_point(*touch.pos):
                        click_event()
                        return True  # ✅ Stops event propagation if needed
                    return super(label.__class__, label).on_touch_down(touch)  # ✅ Call original method 
                self.info_label.on_touch_down = MethodType(on_touch_down, self.info_label)
                account_info = f"[u]{account_info}[/u]"
                
            self.account_info = account_info

class AccountNumberNameLayout(BoxLayout):
    account_image : str = StringProperty('')

    def setup_image(self, account_image = None): 
        # ✅ Set the background image path BEFORE adding widgets
        if (account_image):
            
            return
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        self.account_image = os.path.join(parent_dir, 'assets', 'account_image.png') 
        print("account_image : ", self.account_image)
         


class TicketTransactionScreeen(Screen):
    
    
    remarks_list : ListProperty = ListProperty([]) 
    
         
    main_parent : FloatLayout = ObjectProperty(None)
    text_input_font_size : int = NumericProperty(0)
    title_font_size : int = NumericProperty(0)
    back_image: Image = ObjectProperty(None)
    back_text: Button = ObjectProperty(None)
    go_back_screen_font_size = NumericProperty(0)  # ✅ Initialize with 0 (Will update later)
    go_back_icon : str = StringProperty('')
    account_name : AccountNumberNameLayout = ObjectProperty(None)
    
    account_name_info : AccountInfoLayout = ObjectProperty(None)
    account_email : AccountInfoLayout = ObjectProperty(None) 
    account_loc1 : AccountInfoLayout = ObjectProperty(None)
    account_loc2 : AccountInfoLayout = ObjectProperty(None)
    account_loc3 : AccountInfoLayout = ObjectProperty(None)
    account_phone1 : AccountInfoLayout = ObjectProperty(None)
    account_phone2 : AccountInfoLayout = ObjectProperty(None)
    account_phone3 : AccountInfoLayout = ObjectProperty(None)
    
    remarks_input : RemarksInputLayout = ObjectProperty(None)
    remarks_list : RemarksListViewer = ObjectProperty(None)
    
    
    view_remarks_button : Button = ObjectProperty(None)
    add_remarks_button : Button = ObjectProperty(None)
    
    
    refresh_layout : CustomScrollView = ObjectProperty(None)
    
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        parent_dir = os.path.dirname(os.path.dirname(__file__)) 
        
        self.go_back_icon = os.path.join(parent_dir, 'assets', 'go_back_icon.png')
        print("go back icon", self.go_back_icon)
        self.bind(size=self.update_size)  # Bind window resize event
        
        
        self.remarks_input = RemarksInputLayout()
        self.remarks_list = RemarksListViewer()
        
        
         
    
    def on_parent(self, *args):
        if self.parent:
            self.refresh_layout.setup_effect_callback(self.refresh_callback) 
            self.view_remarks_button.on_release= self.remarks_list.open
            self.add_remarks_button.on_release= self.remarks_input.open
            self.main_parent.height = self.parent.height - dp(65)
      
    def refresh_callback(self, *args):
        print("refresh_callback : Ticket Transact")
 
    def update_size(self, *args):
        """ Update circle size dynamically when window size changes """  
        self.body_font_size = min(Window.width, Window.height) * 0.04
        self.title_font_size = min(Window.width, Window.height) * 0.05
        self.go_back_screen_font_size = min(Window.width, Window.height) * 0.04
        print("update_size : ", self.text_input_font_size)

    def on_leave(self, *args):
        Animation(opacity=0, duration=0.5).start(self)
        return super().on_leave(*args)
    
    def on_enter(self, *args):
        Animation(opacity=1, duration=0.5).start(self)
        
        # self.manager.proccess_layout.open() # Use it only if when proccessing a layout
        
        self.account_name_info.setup(icon_image='account-box' , account_info="Tech Makie Catamora")
        self.account_email.setup(icon_image='email' , account_info="techmakie@gmail.com")
        
        def setup_location_1():
            self.open_google_maps(14.5995, 120.9842)
            
        self.account_loc1.setup(icon_image='google-maps' , account_info="123 Main St, San Francisco, CA" , click_event=setup_location_1)
        
        self.account_loc2.setup( account_info="456 Elm St, San Francisco, CA", click_event=setup_location_1)
        
        self.account_loc3.setup( account_info="789 Oak St, San Francisco, CA", click_event=setup_location_1)
        
        
        self.account_phone1.setup(icon_image='phone' , account_info="123-456-7890")
        self.account_phone2.setup(account_info="987-654-3210")
        self.account_phone3.setup(account_info="098-765-4321")
        
        self.back_text.on_press=self.go_back
            
        def on_touch_down(image, touch):
            """ Detect touch inside the image """
            if image.collide_point(*touch.pos):
                self.go_back()
                return True  # ✅ Stops event propagation if needed
            return super(image.__class__, image).on_touch_down(touch)  # ✅ Call original method

        # ✅ Bind on_touch_down correctly
        self.back_image.on_touch_down = MethodType(on_touch_down, self.back_image)
        
        self.account_name.setup_image()  # ✅ Set the background image path before adding widgets
        
        
        return super().on_enter(*args)
    
    def go_back(self, *args): 
        self.manager.transition.duration= 0.5
        self.manager.transition.direction = "right"
        self.manager.current = HOME_SCREEN_TICKETLIST_SCREEN
    
    
    def open_google_maps(self, destination_lat, destination_lon):
        """ Opens Google Maps with directions from current location to a given destination. """
        url = f"https://www.google.com/maps/dir/?api=1&origin=current+location&destination={destination_lat},{destination_lon}"
        webbrowser.open(url)
        