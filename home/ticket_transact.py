from kivymd.uix.chip.chip import MDIcon
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
from kivy_garden.mapview import MapView
import os
from kivy.clock import Clock
from kivy.uix.modalview import ModalView
from kivy_garden.mapview import MapView, MapSource
from kivy.uix.image import Image
from kivy.properties import ObjectProperty, NumericProperty

from kivy.utils import get_color_from_hex as chex
from kivy.core.clipboard import Clipboard
from kivy.utils import platform
from utils.app_utils import is_valid_latlon

if platform == "android":
    from plyer import gps
    from kivymd.toast import toast


from kivy_garden.mapview import MapView, MapSource  # Make sure mapview is installed

# Optional: Custom tile server or use default
map_source = MapSource(url="http://c.tile.openstreetmap.org/{z}/{x}/{y}.png",
                       cache_key="osm",
                       tile_size=256,
                       image_ext="png")








class POCLayout(MDBoxLayout):
    is_not_done : bool = BooleanProperty(True)
    step_text : str = StringProperty('Step 4: Submit Proof of Completion')
















class FiberConnectionModalView(ModalView):
    rx : TextInput = ObjectProperty(None)
    tx : TextInput = ObjectProperty(None)
    parent_event : object = ObjectProperty(None)
    rx_level : str = StringProperty('Not yet documented')
    tx_level : str = StringProperty('Not yet documented')

    def on_kv_post(self, base_widget):
        self.rx.bind(text=self.on_rx_change)
        self.tx.bind(text=self.on_tx_change)
    
    def on_rx_change(self, instance, value):
        self.rx_level = value
        self.parent_event(rx = self.rx_level, tx = self.tx_level)
    
    def on_tx_change(self, instance, value):
        self.tx_level = value
        self.parent_event(rx = self.rx_level, tx = self.tx_level)


class FiberConnectionStepLayout(MDBoxLayout): 
    is_not_done : bool = BooleanProperty(True)
    step_text : str = StringProperty('Step 3: Fiber Connection Check')
    is_valid_level : bool = BooleanProperty(False)
    set_fiber_button : Button = ObjectProperty(None)
    next_step_button : Button = ObjectProperty(None) 
    is_accessible : bool = BooleanProperty(False)

    tx_level : str = StringProperty('Not yet documented')
    rx_level : str = StringProperty('Not yet documented')

    original_height = NumericProperty(320)

    parent_event : object = ObjectProperty(None)

    def update_level(self, tx, rx):
        self.tx_level = tx
        self.rx_level = rx
        if str(tx).isdigit() and str(rx).isdigit():
            self.is_valid_level = True
        else:
            self.is_valid_level = False


    def display_none(self, *args):
        self.is_accessible = False
        self.next_step_button.disabled = True
        self.set_fiber_button.disabled = True

        # Just fade out and make invisible
        Animation(opacity=0, duration=0.3 , height=0).start(self)


    def display_block(self, *args):
        self.is_accessible = True
        self.next_step_button.disabled = False
        self.set_fiber_button.disabled = False

        # Restore opacity
        Animation(opacity=1, duration=0.3, height=dp(self.original_height)).start(self)

 

class GeolocationModalView(ModalView):
    map = ObjectProperty(None)
    lat : str = StringProperty('[font=roboto_semibold]Latitude :[/font] [font=roboto_light]0[/font]')
    lon : str = StringProperty('[font=roboto_semibold]Longitude :[/font] [font=roboto_light]0[/font]')
    lon_data : float = NumericProperty(0)
    lat_data : float = NumericProperty(0)
    location_input : TextInput = ObjectProperty(None)
    is_valid_location : bool = BooleanProperty(False)

    parent_event : object = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mapview = None  # 👈 store MapView instance
    
    def on_parent(self, *args):
        Clock.schedule_once(self.load_map, 0.3)

    def on_kv_post(self, base_widget):
        # Ensure location_input is set and bind an event
        if self.location_input:
            self.location_input.bind(text=self.on_location_change)


    def on_location_change(self, instance, value):
        print(f"📍 Location input changed to: {value}")
        if is_valid_latlon(value):
            self.is_valid_location = True 
            lat_str, lon_str = value.split(",")
            lat = float(lat_str.strip())
            lon = float(lon_str.strip())
            self.go_to_location(lat, lon)
        else:
            self.is_valid_location = False

    def on_open(self, *args):
        if self.lat_data == 0 or self.lon_data == 0:
            if platform == "android":
                try:
                    gps.configure(on_location=self.gps_callback, on_status=self.gps_status)
                    gps.start(minTime=1000, minDistance=1)
                except NotImplementedError:
                    print("GPS not implemented on this platform")
            else:
                self.go_to_location(12.375466976256769, 123.63299577874449)  # fallback

    def gps_status(self, status_type, status):
        print(f"GPS Status → {status_type}: {status}")
    
    def gps_callback(self, **kwargs):
        self.lat_data = float(kwargs.get('lat', 0))
        self.lon_data = float(kwargs.get('lon', 0))
        print(f"📡 GPS location received → Lat: {self.lat_data}, Lon: {self.lon_data}")
        self.go_to_location(self.lat_data, self.lon_data)
        gps.stop()  # Stop after getting one location fix

    def load_map(self, *args):
        if not self.ids.map.children:
            self.mapview = MapView(lat=12.375466976256769, lon=123.63299577874449, zoom=25,
                              map_source=map_source,
                              size_hint=(1, 1),
                              pos_hint={"center_x": 0.5, "center_y": 0.5})
             # Optional: bind to map position updates
            self.mapview.bind(lat=self.on_map_move, lon=self.on_map_move)

            self.map.add_widget(self.mapview)
            marker_icon = MDIcon(icon="home-map-marker",
                                 font_size=sp(58), 
                                 theme_text_color="Custom",
                                 text_color=chex("#B71E1E"),
                                 pos_hint={"center_x": 0.5, "center_y": 0.5}
                                 )
            self.map.add_widget(marker_icon)

    def on_map_move(self, *args):
        """ Called when user pans the map. """
        if self.mapview:
            self.lat_data = self.mapview.lat
            self.lon_data = self.mapview.lon 
            print(f"📍 Map center updated → Lat: {self.lat_data}, Lon: {self.lon_data}")
            self.parent_event(lat_data = self.lat_data, lon_data = self.lon_data)
            lat = f"{round(self.lat_data, 10)}.." if len(str(self.lat_data)) > 10 else self.lat_data
            lon = f"{round(self.lon_data, 10)}.." if len(str(self.lon_data)) > 10 else self.lon_data
            self.lat = f"[font=roboto_semibold]Latitude :[/font] [font=roboto_light]{lat}[/font]"
            self.lon = f"[font=roboto_semibold]Longitude :[/font] [font=roboto_light]{lon}[/font]"
            
    def get_center_coords(self):
        """ Call this when you want to access the map center directly. """
        if self.mapview:
            return self.mapview.lat, self.mapview.lon
        return None, None

    def go_to_location(self , new_lat , new_lon): 
        self.lat_data = new_lat
        self.lon_data = new_lon
        if self.mapview:
            self.mapview.center_on(new_lat, new_lon)
            self.mapview.zoom = 25  # Optional: adjust zoom for better clarity
        else:
            Clock.schedule_once(self.load_map, 0.3)
            Clock.schedule_once( lambda *args: self.go_to_location(new_lat, new_lon), 0.3)
    



class GeolocationStepLayout(MDBoxLayout):
    is_not_done : bool = BooleanProperty(True)
    step_text : str = StringProperty('Step 2: Geo-Mapping Submission')
    set_location_button : Button = ObjectProperty(None)
    next_step_button : Button = ObjectProperty(None)
    longitude : str = StringProperty('0')
    latitude : str = StringProperty('0')
    location_info : BoxLayout = ObjectProperty(None)
    is_accessible : bool = BooleanProperty(False)

    original_height = NumericProperty(320)

    parent_event : object = ObjectProperty(None)


    def __init__(self, **kwargs):
        super().__init__(**kwargs) 

        
    def display_none(self, *args):
        self.is_accessible = False
        self.next_step_button.disabled = True
        self.set_location_button.disabled = True

        # Just fade out and make invisible
        Animation(opacity=0, duration=0.3 , height=0).start(self)


    def display_block(self, *args):
        self.is_accessible = True
        self.next_step_button.disabled = False
        self.set_location_button.disabled = False

        # Restore opacity
        Animation(opacity=1, duration=0.3, height=dp(self.original_height)).start(self)


    def update_location(self, lat_data, lon_data):
        self.longitude = str(lon_data)
        self.latitude = str(lat_data)
 
     

    def on_touch_down(self, touch):
        # Check if the touch was inside location_info
        if self.location_info and self.location_info.collide_point(*touch.pos):
            Clipboard.copy(f"{self.latitude}, {self.longitude}")
            print(f"📋 Copied to clipboard: {self.latitude}, {self.longitude}")
            if platform == "android": 
                toast("📍 Coordinates copied to clipboard!")
            else:
                print("📍 Coordinates copied to clipboard!")  # fallback on desktop
            return True  # Swallow the touch event
        return super().on_touch_down(touch)
    



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

    geolocation_step_layout : GeolocationStepLayout = ObjectProperty(None)
    fiber_connection_step_layout : FiberConnectionStepLayout = ObjectProperty(None)
    poc_layout : POCLayout = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        parent_dir = os.path.dirname(os.path.dirname(__file__)) 
        
        self.go_back_icon = os.path.join(parent_dir, 'assets', 'go_back_icon.png')
        print("go back icon", self.go_back_icon)
        self.bind(size=self.update_size)  # Bind window resize event
        
        
        self.remarks_input = RemarksInputLayout()
        self.remarks_list = RemarksListViewer()
        self.geolocation_modal = GeolocationModalView()
        self.fiber_connection_modal = FiberConnectionModalView()
        
    
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



        self.geolocation_step_layout.parent_event = self.geolocation_modal.open
        self.geolocation_modal.parent_event = self.geolocation_step_layout.update_location

        self.fiber_connection_step_layout.parent_event = self.fiber_connection_modal.open
        self.fiber_connection_modal.parent_event = self.fiber_connection_step_layout.update_level


        # self.geolocation_modal.open()
        
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
        