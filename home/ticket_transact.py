from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.accordion import DictProperty
from kivymd.uix.chip.chip import MDIcon
from kivy.uix.behaviors import ButtonBehavior
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
from kivy.properties import ObjectProperty, NumericProperty, DictProperty

from kivy.utils import get_color_from_hex as chex
from kivy.core.clipboard import Clipboard
from kivy.utils import platform
from utils.app_utils import is_valid_latlon
from kivy.uix.image import Image
from utils.app_utils import has_internet
from kivymd.app import MDApp
import shutil

if platform == "android":
    from plyer import gps
    from kivymd.toast import toast
from kivy import platform
import os

if platform == "win":
    from plyer import filechooser
if platform == "android":
    from android.storage import app_storage_path
    from androidstorage4kivy import SharedStorage, Chooser

import random
from utils.app_utils import image_path_to_base64, is_image, is_image_ext

from kivy_garden.mapview import MapView, MapSource  # Make sure mapview is installed

# Optional: Custom tile server or use default
# map_source = MapSource(url="http://c.tile.openstreetmap.org/{z}/{x}/{y}.png",
#                        cache_key="osm",
#                        tile_size=256,
#                        image_ext="png")
map_source = MapSource(
    url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    cache_key="satellite",
    tile_size=256,
    image_ext="jpg",  # Esri tiles are usually JPG
    attribution="Tiles © Esri — Source: Esri, Earthstar Geographics"
)


class ForReviewLayout(MDBoxLayout):
    step_text : str = StringProperty('Step 5: Submit for Review') 
    is_not_done : bool = BooleanProperty(True)  
    is_accessible : bool = BooleanProperty(False)
    is_ready : bool = BooleanProperty(False)
    procced_event : object = ObjectProperty(None)

    def display_none(self, *args):
        self.is_accessible = False 

        # Just fade out and make invisible
        Animation(opacity=0, duration=0.3 ).start(self)


    def display_block(self, *args):
        self.is_accessible = True 

        # Restore opacity
        Animation(opacity=1, duration=0.3).start(self)

 

class ClickableIcon(ButtonBehavior, MDIcon):
    pass

class POCImageLayout(Image):
    image_path : str = StringProperty('') 
    parent_event : object = ObjectProperty(None)
    index : str = StringProperty('')
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        image_path = kwargs.get('image_path', '')
        self.index = kwargs.get('index', '')
        if image_path:
            self.image_path = image_path
        else:
            parent_dir = os.path.dirname(os.path.dirname(__file__)) 
            self.image_path = os.path.join(parent_dir, 'assets', 'app_logo.png')
    
    # def on_parent(self, *args):
    #     parent_dir = os.path.dirname(os.path.dirname(__file__)) 
        # self.image_path = os.path.join(parent_dir, 'assets', 'app_logo.png')
        # print("image_path", self.image_path)


    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            Animation(opacity=0, duration=0.3).start(self)
            self.parent_event(self.index)
            Clock.schedule_once(lambda dt: self.parent.remove_widget(self), 0.3)
            return True
        return super().on_touch_down(touch)
    
    
    


# TODO: Add event to the add_poc_image_button
class POCUploaderLayout(MDBoxLayout):
    original_height : int = NumericProperty(140)
    step_text : str = StringProperty('1. Costumer Proof Signature.')
    step_instruction : str = StringProperty("Instructions : Upload an image of the customer's signed proof of service completion.")
    is_accessible : bool = BooleanProperty(False)

    parent_event = ObjectProperty(None)
    selected_images = DictProperty({}) # {index: image_path}
    poc_images_container : BoxLayout = ObjectProperty(None)
    is_selecting_file : bool = BooleanProperty(False)
    
    def setup_poc_uploader_layout(self, step_text, step_instruction):
        self.step_text = step_text
        self.step_instruction = step_instruction
        self.selected_images = {}
        self.poc_images_container.clear_widgets()


    def display_none(self, *args):
        self.is_accessible = False 

        # Just fade out and make invisible
        Animation(opacity=0, duration=0.3 , height=0).start(self)


    def display_block(self, *args):
        self.is_accessible = True 

        # Restore opacity
        Animation(opacity=1, duration=0.3, height=dp(self.original_height)).start(self)

    def delete_image(self, index):
        if index in self.selected_images:
            del self.selected_images[index]
            self.parent_event()

    def upload_image(self):
        if self.is_selecting_file:
            return
        self.is_selecting_file = True
        
        def reset_selecting(*args):
            self.is_selecting_file = False

        Clock.schedule_once( reset_selecting  , 1)

        if platform == "win":
            filechooser.open_file(on_selection=self.handle_selection)
        elif platform == "android":
            # SharedStorage().choose_file(mime_type="image/*", callback=self.on_image_selected)
            self.chooser = Chooser(self.on_image_selected)
            self.chooser.choose_content('image/*', multiple=False)

    def handle_selection(self, selection):
        if selection:
            image_path = selection[0]  # Display the selected image
            if not is_image(image_path):
                if platform == "android":
                    toast("Invalid image format. Please select a valid image file.") 
                return
            index = ''.join(random.choices('0123456789', k=5))
            self.selected_images[index] = image_path
            image = POCImageLayout(image_path=image_path, index=index)
            image.parent_event = self.delete_image
            self.poc_images_container.add_widget(image)
            self.parent_event()
            self.is_selecting_file = False
        else:
            self.is_selecting_file = False

    def on_image_selected(self, uri_list):
        if uri_list:
            uri = uri_list[0]
            ss = SharedStorage()

            # ✅ Copy file from shared storage to app cache
            private_file_path = ss.copy_from_shared(uri)
            if private_file_path: 
                Clock.schedule_once(lambda dt: self.on_image_loaded_path(private_file_path))
            else:
                if platform == "android":
                    toast("Failed to load image from storage.")
                self.is_selecting_file = False
        else:
            self.is_selecting_file = False

    def on_image_loaded_path(self, private_file_path):
        filename = os.path.basename(private_file_path)

        # ✅ Check if it's an image
        if not is_image_ext(filename):
            if platform == "android":
                toast("Invalid image format. Please select a valid image file.")
            self.is_selecting_file = False
            return

        save_dir = os.path.join(self.get_save_path(), "selected_images")
        os.makedirs(save_dir, exist_ok=True)

        image_path = os.path.join(save_dir, filename)

        # ✅ Copy file to save location
        shutil.copy(private_file_path, image_path)

        # ✅ Update UI
        index = ''.join(random.choices('0123456789', k=5))
        self.selected_images[index] = image_path
        image = POCImageLayout(image_path=image_path, index=index)
        image.parent_event = self.delete_image
        self.poc_images_container.add_widget(image)
        self.parent_event()
        self.is_selecting_file = False
        print(f"✅ Saved and loaded image path (Android): {image_path}")

    def get_save_path(self):
        # Return a writable path depending on the platform
        if platform == "android": 
            return app_storage_path()
        else:
            return os.path.expanduser("~")

class POCFileUploaderModalView(ModalView):
    file_image_path : str = StringProperty('')
    temp_parent : POCUploaderLayout = ObjectProperty(None)

    def on_parent(self, *args):
        parent_dir = os.path.dirname(os.path.dirname(__file__)) 
        self.file_image_path = os.path.join(parent_dir, 'assets', 'upload_image.png')
        # print("file_image_path", self.file_image_path)


    def activate_account(self, temp_parent : POCUploaderLayout):
        self.temp_parent = temp_parent
        self.open()


class POCLayout(MDBoxLayout):
    is_not_done : bool = BooleanProperty(True)
    step_text : str = StringProperty('Step 4: Submit Proof of Completion')



    def display_none(self, *args):
        # Just fade out and make invisible
        Animation(opacity=0, duration=0.3 ).start(self)


    def display_block(self, *args):
        # Restore opacity
        Animation(opacity=1, duration=0.3 ).start(self)




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
    procced_event : object = ObjectProperty(None)

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
        if platform == "android":
            try:
                gps.configure(on_location=self.gps_callback, on_status=self.gps_status)
                gps.start(minTime=1000, minDistance=1)
            except NotImplementedError:
                print("GPS not implemented on this platform")
                self.go_to_location(12.367796960, 123.62151820)
            except Exception as e:
                print(f"Error starting GPS: {e}")
                self.go_to_location(12.367796960, 123.62151820)
        else:
            self.go_to_location(12.367796960, 123.62151820)  # fallback

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
            
            if not has_internet():
                return
            
            self.mapview = MapView(lat=12.367796960, lon=123.62151820, zoom=25,
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
        try:
            if self.mapview:
                self.mapview.center_on(new_lat, new_lon)
                self.mapview.zoom = 16  # Optional: adjust zoom for better clarity
                self.mapview.min_zoom = 1
                self.mapview.max_zoom = 17
            else:
                Clock.schedule_once(self.load_map, 0.3)
                Clock.schedule_once( lambda *args: self.go_to_location(new_lat, new_lon), 0.3)
        except Exception as e:
            print(f"Error: {e}")
        



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
    procced_event : object = ObjectProperty(None)


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

    def is_okey_to_proceed(self, *args):
        if not self.is_accessible:
            return False
        if not self.latitude or not self.longitude:
            return False
        if self.latitude == '0' or self.longitude == '0':
            return False
        if not self.is_not_done:
            return False
        return True

    def update_location(self, lat_data, lon_data):
        self.longitude = str(lon_data)
        self.latitude = str(lat_data)
    
    def get_data(self):
        if self.latitude and self.longitude:
            return float(self.latitude), float(self.longitude)
        else:
            return None
     

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
    
    parent_event : object = ObjectProperty(None)
    next_step_button : Button = ObjectProperty(None)
    adjusting_height = ObjectProperty(dp(95))
    
    def on_touch_down(self, touch):
        if self.next_step_button and self.next_step_button.collide_point(*touch.pos): 
            # You can manually call its on_release or do any action
            if self.parent_event:
                self.parent_event()
                # print(f"parent_event: Yahooo")
                # pass
            # self.next_step_button.dispatch('on_release')  # Optional: simulate normal click
            return True  # Stop the touch here if needed (so it doesn't pass through)

        return super().on_touch_down(touch)
    def reset_layout(self):
        self.is_not_done = True 

    def has_next(self):
        self.adjusting_height = dp(40)

    def has_no_next(self):
        self.adjusting_height = dp(95)




class Remark(BoxLayout):
    remark_text : str = StringProperty('This is a remark')
    remark_id : int = NumericProperty(0)


class RemarksListViewer(ModalView):
    
    remarks_list_view : BoxLayout = ObjectProperty(None)

    def clean_remarks_list_view(self):
        self.remarks_list_view.clear_widgets()

    def add_remarks(self, title : str, remarks : str , rdate : str , by : str, rid : int):
        remark = Remark()
        remark.remark_id = rid
        remark.remark_text = f"[font=roboto_semibold]TITLE: [/font] {title}\n[font=roboto_semibold]Content: [/font] {remarks} \n[font=roboto_semibold]DATE: [/font] {rdate} \n[font=roboto_semibold]ADDED BY: [/font] {by}"
        self.remarks_list_view.add_widget(remark , index=len(self.remarks_list_view.children))

    def add_remarks_from_list(self, remarks_list : list):
        self.clean_remarks_list_view()
        for remark in remarks_list:
            self.add_remarks(remark['title'], remark['remark'], remark['remark_date'], remark['remark_by'], remark['remark_by_id'])
     

class RemarksInputLayout(ModalView):
    remark_text : TextInput = ObjectProperty(None)
    title_remark : TextInput = ObjectProperty(None)
    is_ready_to_submit : bool = BooleanProperty(False)
    parent_obj : object = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.remark_text.bind(text=self.on_text_change)
        self.title_remark.bind(text=self.on_text_change)
    
    def on_open(self):
        self.remark_text.focus = True
    
    def on_text_change(self, instance, value):
        if len(self.remark_text.text) > 0 and len(self.title_remark.text) > 0:
            self.is_ready_to_submit = True
        else:
            self.is_ready_to_submit = False
    
    def submit_remarks(self):
        key = "ADD_REMARKS" 
        app = MDApp.get_running_app()
        if key in app.communications.key_running:
            return 
        self.parent_obj.manager.proccess_layout.open() 
        app.communications.add_remarks( self.parent_obj.ticket.get('ticket_id'), self.title_remark.text , self.remark_text.text )
        def communication_event(*args):
            data = app.communications.get_and_remove(key)  
            if data.get("result", None): 
                self.parent_obj.manager.proccess_layout.display_success(data.get("message"))
                self.title_remark.text = ""
                self.remark_text.text = ""
                Clock.schedule_once(self.parent_obj.refetch_remarks, 0.5)
                return False
            elif data.get("result", False) == False: 
                self.parent_obj.manager.proccess_layout.display_error(data.get("message")) 
                return False
            elif data.get("result", False) == None:
                self.parent_obj.manager.proccess_layout.display_error(data.get("message"))
                return False
                

        Clock.schedule_interval(communication_event, 1)


class AccountInfoLayout(MDBoxLayout):
    icon_image : str = StringProperty('')
    account_info : str = StringProperty("......")
    click_event : object = ObjectProperty(None)
    
    info_label : BoxLayout = ObjectProperty(None)
    info_color : str = StringProperty('')
    
    def setup(self, icon_image = None, account_info = None , click_event = None, color = None):
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
            else:
                def on_touch_down(label, touch):
                    """ Detect touch inside the image """
                    if label.collide_point(*touch.pos):
                        # click_event()
                        return True  # ✅ Stops event propagation if needed
                    return super(label.__class__, label).on_touch_down(touch)  # ✅ Call original method 
                self.info_label.on_touch_down = MethodType(on_touch_down, self.info_label)
            self.account_info = account_info
        if (color):
            self.info_color = color

class AccountNumberNameLayout(BoxLayout):
    account_image : str = StringProperty('')
    ticket_number : str = StringProperty('')

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
    # account_loc2 : AccountInfoLayout = ObjectProperty(None)
    # account_loc3 : AccountInfoLayout = ObjectProperty(None)
    account_phone1 : AccountInfoLayout = ObjectProperty(None)
    account_phone2 : AccountInfoLayout = ObjectProperty(None)
    account_phone3 : AccountInfoLayout = ObjectProperty(None) 
    state_widget : AccountInfoLayout = ObjectProperty(None)
    details_widget : AccountInfoLayout = ObjectProperty(None)
    
    remarks_input : RemarksInputLayout = ObjectProperty(None)
    remarks_list : RemarksListViewer = ObjectProperty(None)
    
    
    view_remarks_button : Button = ObjectProperty(None)
    add_remarks_button : Button = ObjectProperty(None)
    
    
    refresh_layout : CustomScrollView = ObjectProperty(None)

    geolocation_step_layout : GeolocationStepLayout = ObjectProperty(None)
    fiber_connection_step_layout : FiberConnectionStepLayout = ObjectProperty(None)
    poc_layout : POCLayout = ObjectProperty(None)

    step1_layout : Step1Layout = ObjectProperty(None)
    poc_uploader_layout_1 : POCUploaderLayout = ObjectProperty(None)
    poc_uploader_layout_2 : POCUploaderLayout = ObjectProperty(None)
    poc_uploader_layout_3 : POCUploaderLayout = ObjectProperty(None)
    poc_uploader_layout_4 : POCUploaderLayout = ObjectProperty(None)
    poc_uploader_layout_5 : POCUploaderLayout = ObjectProperty(None)
    poc_uploader_layout_6 : POCUploaderLayout = ObjectProperty(None)
    poc_uploader_layout_7 : POCUploaderLayout = ObjectProperty(None)
    poc_uploader_layout_8 : POCUploaderLayout = ObjectProperty(None)
    poc_uploader_layout_9 : POCUploaderLayout = ObjectProperty(None)
    poc_uploader_layout_10 : POCUploaderLayout = ObjectProperty(None)
    poc_uploader_layout_11 : POCUploaderLayout = ObjectProperty(None)
    poc_uploader_layout_12 : POCUploaderLayout = ObjectProperty(None)
    poc_uploader_layout_13 : POCUploaderLayout = ObjectProperty(None)
    poc_uploader_layout_14 : POCUploaderLayout = ObjectProperty(None)
    for_review_layout : ForReviewLayout = ObjectProperty(None)

    ticket : dict = DictProperty({})
    images_data : dict = DictProperty({})
    # images_data = { poc : { index : image_path , ... }}
    back_pressed_once = False
    has_changed_data : bool = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        parent_dir = os.path.dirname(os.path.dirname(__file__)) 
        
        self.go_back_icon = os.path.join(parent_dir, 'assets', 'go_back_icon.png')
        print("go back icon", self.go_back_icon)
        self.bind(size=self.update_size)  # Bind window resize event
        
        
        self.remarks_input = RemarksInputLayout()
        self.remarks_input.parent_obj = self
        self.remarks_list = RemarksListViewer()
        self.geolocation_modal = GeolocationModalView()
        self.fiber_connection_modal = FiberConnectionModalView()
        self.poc_file_uploader_modal = POCFileUploaderModalView()

        Window.bind(on_keyboard=self.on_back_key)

    def on_back_key(self, window, key, *args):
        if key != 27:
            return False

        if self.manager.proccess_layout.is_open:
            return True

        if self.manager.current == HOME_SCREEN_TRANSACT_SCREEN:
            self.go_back()
            return True
        else: 
            if not self.back_pressed_once:
                self.back_pressed_once = True
                if platform == 'android':
                    toast("Press back again to exit") 
                    
                Clock.schedule_once(self.reset_back_state, 2)
                return True
            else:
                self.stop_app()
                return True
 

    def reset_back_state(self, dt):
        self.back_pressed_once = False

    def stop_app(self):
        MDApp.get_running_app().stop()

    def on_parent(self, *args):
        if self.parent:
            self.refresh_layout.setup_effect_callback(self.refresh_callback) 
            self.view_remarks_button.on_release= self.remarks_list.open
            self.add_remarks_button.on_release= self.remarks_input.open
            # self.main_parent.height = self.parent.height - dp(65)
      
    def refresh_callback(self, *args):
        print("refresh_callback : Ticket Transact")
 
    def update_size(self, *args):
        """ Update circle size dynamically when window size changes """  
        self.body_font_size = min(Window.width, Window.height) * 0.04
        self.title_font_size = min(Window.width, Window.height) * 0.05
        self.go_back_screen_font_size = min(Window.width, Window.height) * 0.03
        print("update_size : ", self.text_input_font_size)

        

    def on_leave(self, *args):
        
        Animation(height=dp(60), opacity = 1, duration=0.5).start(self.manager.parent.navigation_bar)
        Animation(opacity=0, duration=0.5).start(self)
        return super().on_leave(*args)
    
    def on_enter(self, *args):
        self.back_pressed_once = False
        Animation(height=dp(-10), opacity = 0, duration=0.5).start(self.manager.parent.navigation_bar)
        Animation(opacity=1, duration=0.5).start(self)

        self.remarks_list.clean_remarks_list_view()
        # self.poc_file_uploader_modal.open()
        print("on_enter : Ticket Transact" , self.ticket)
        if not self.ticket:
            self.go_back()
        self.images_data = {}
        self.geolocation_step_layout.parent_event = self.geolocation_modal.open
        self.geolocation_modal.parent_event = self.geolocation_step_layout.update_location

        self.fiber_connection_step_layout.parent_event = self.fiber_connection_modal.open
        self.fiber_connection_modal.parent_event = self.fiber_connection_step_layout.update_level

        self.setup_poc_uploader_layout()
 
        
        # self.manager.proccess_layout.open() # Use it only if when proccessing a layout
        self.account_name.ticket_number = self.ticket.get("ticketnumber", "N/A")
        self.account_name_info.setup(icon_image='account-box' , account_info=self.ticket.get( "client_name" , "N/A"))
        self.account_email.setup(icon_image='email' , account_info=self.ticket.get( "email" ,"N/A"))


        # def setup_location_2():
        #     lat, lng = self.ticket.get("lat_2", 14.5995), self.ticket.get("lng_2", 120.9842)
        #     self.open_google_maps(14.5995, 120.9842)
            
        # def setup_location_3():
        #     lat, lng = self.ticket.get("lat_3", 14.5995), self.ticket.get("lng_3", 120.9842)
        #     self.open_google_maps(14.5995, 120.9842)

        geomap = self.ticket.get("geomap", [14.5995, 120.9842])
        
        if geomap:
            def setup_location_1():
                lat, lng = geomap
                self.open_google_maps(lat, lng)

            self.account_loc1.setup(icon_image='google-maps' , account_info=self.ticket.get( "address", "N/A") , click_event=setup_location_1)
        else:
            self.account_loc1.setup(icon_image='google-maps' , account_info=self.ticket.get( "address", "N/A"), click_event=None)
        
        # self.account_loc2.setup( account_info=self.ticket.get( "address2", "N/A"), click_event=setup_location_2)
        
        # self.account_loc3.setup( account_info=self.ticket.get( "address3", "N/A"), click_event=setup_location_3)
        
        self.account_phone1.setup(icon_image='phone' , account_info=self.ticket.get( "primary_contact", "N/A"))
        self.account_phone2.setup(account_info=self.ticket.get( "phone2", "N/A"))
        self.account_phone3.setup(account_info=self.ticket.get( "phone3", "N/A"))

        state = self.ticket.get( "state", "N/A")
        self.state_widget.setup(
            icon_image='alert-circle-check' if state == "Normal" else 'alert-octagram' ,
            account_info= "Normal" if state == "Normal" else state,
            color= '#5CBA45' if state == "Normal" else '#B71E1E'
            )
        self.details_widget.setup(icon_image='information' , account_info=self.ticket.get( "detail", "N/A"))
        
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
        

        self.display_by_step(self.ticket.get("step", 1))
        # self.display_by_step(4)

        def display_the_remaks(*args):
            remarks = self.ticket.get("remarks", [])
            self.remarks_list.add_remarks_from_list(remarks)
        
        Clock.schedule_once(display_the_remaks, 0.5)
        return super().on_enter(*args)
    




    def go_back(self, *args): 
        self.manager.transition.duration= 0.5
        self.manager.transition.direction = "right"
        self.manager.current = HOME_SCREEN_TICKETLIST_SCREEN
    
    
    def open_google_maps(self, destination_lat, destination_lon):
        """ Opens Google Maps with directions from current location to a given destination. """
        url = f"https://www.google.com/maps/dir/?api=1&origin=current+location&destination={destination_lat},{destination_lon}"
        webbrowser.open(url)
    

    def setup_poc_uploader_layout(self, *args):
        self.poc_uploader_layout_1.setup_poc_uploader_layout(
            step_text="1. Costumer Proof Signature",
            step_instruction="Instructions : Upload an image of the customer's signed proof of service completion."
        )
        self.poc_uploader_layout_2.setup_poc_uploader_layout(
            step_text="2. Terminal Box",
            step_instruction="Instructions : Provide a clear image of the installed terminal box."
        )
        self.poc_uploader_layout_3.setup_poc_uploader_layout(
            step_text="3. Terminal Box Fiber Tag/Labe",
            step_instruction="Instructions :Capture the fiber tag or labeling on the terminal box."
        )
        self.poc_uploader_layout_4.setup_poc_uploader_layout(
            step_text="4. Serial Number of Modem/Device",
            step_instruction="Instructions : Upload an image showing the serial number of the modem or device."
        )
        self.poc_uploader_layout_5.setup_poc_uploader_layout(
            step_text="5. Modem Setup",
            step_instruction="Instructions : Take a picture of the properly installed modem."
        )
        self.poc_uploader_layout_6.setup_poc_uploader_layout(
            step_text="6. Modem/Device Configuration",
            step_instruction="Instructions : Provide a screenshot or image of the configured modem settings."
        )
        self.poc_uploader_layout_7.setup_poc_uploader_layout(
            step_text="7. RX and TX Signal Levels",
            step_instruction="Instructions : Upload an image displaying the RX and TX signal levels."
        )
        self.poc_uploader_layout_8.setup_poc_uploader_layout(
            step_text="8. Signal PON Meter Reading",
            step_instruction="Instructions : Capture the PON meter reading for verification."
        )
        self.poc_uploader_layout_9.setup_poc_uploader_layout(
            step_text="9. Speed Test (2G Network)",
            step_instruction="Instructions : Upload a screenshot of the speed test results on a 2G network."
        )
        self.poc_uploader_layout_10.setup_poc_uploader_layout(
            step_text="10. Speed Test (5G Network)",
            step_instruction="Instructions : Upload a screenshot of the speed test results on a 5G network."
        )
        self.poc_uploader_layout_11.setup_poc_uploader_layout(
            step_text="11. WiFi Analyzer (2G Network)",
            step_instruction="Instructions : Provide a screenshot of the WiFi analyzer results for the 2G network."
        )
        self.poc_uploader_layout_12.setup_poc_uploader_layout(
            step_text="12. WiFi Analyzer (5G Network)",
            step_instruction="Instructions : Provide a screenshot of the WiFi analyzer results for the 5G network."
        )
        self.poc_uploader_layout_13.setup_poc_uploader_layout(
            step_text="13. Geolocation Upload",
            step_instruction="Instructions : Upload a screenshot of the geolocation coordinates for the installation site."
        )
        self.poc_uploader_layout_14.setup_poc_uploader_layout(
            step_text="14. Upload Completed Ticket Form",
            step_instruction="Instructions : Submit a scanned copy or image of the completed ticket form."
        )
        
        
    
    def display_by_step(self , step : int):
        if step == 1:
            self.step1_layout.is_not_done = True
            self.step1_layout.parent_event = self.next_step_1
            self.step1_layout.has_no_next()
            self.geolocation_step_layout.display_none()
            self.fiber_connection_step_layout.display_none()
            self.poc_layout.display_none()
            self.poc_uploader_layout_1.display_none()
            self.poc_uploader_layout_2.display_none()
            self.poc_uploader_layout_3.display_none()
            self.poc_uploader_layout_4.display_none()
            self.poc_uploader_layout_5.display_none()
            self.poc_uploader_layout_6.display_none()
            self.poc_uploader_layout_7.display_none()
            self.poc_uploader_layout_8.display_none()
            self.poc_uploader_layout_9.display_none()
            self.poc_uploader_layout_10.display_none()
            self.poc_uploader_layout_11.display_none()
            self.poc_uploader_layout_12.display_none()
            self.poc_uploader_layout_13.display_none()
            self.poc_uploader_layout_14.display_none()
            self.for_review_layout.display_none() 
        elif step == 2:
            self.step1_layout.is_not_done = False
            self.step1_layout.parent_event = lambda *args : None
            self.step1_layout.has_next()
            self.geolocation_step_layout.display_block()
            self.geolocation_step_layout.is_not_done = True
            self.geolocation_step_layout.procced_event = self.next_step_2
            self.fiber_connection_step_layout.display_none()
            self.poc_layout.display_none()
            self.poc_uploader_layout_1.display_none()
            self.poc_uploader_layout_2.display_none()
            self.poc_uploader_layout_3.display_none()
            self.poc_uploader_layout_4.display_none()
            self.poc_uploader_layout_5.display_none()
            self.poc_uploader_layout_6.display_none()
            self.poc_uploader_layout_7.display_none()
            self.poc_uploader_layout_8.display_none()
            self.poc_uploader_layout_9.display_none()
            self.poc_uploader_layout_10.display_none()
            self.poc_uploader_layout_11.display_none()
            self.poc_uploader_layout_12.display_none()
            self.poc_uploader_layout_13.display_none()
            self.poc_uploader_layout_14.display_none()
            self.for_review_layout.display_none()
        elif step == 3:
            self.step1_layout.is_not_done = False
            self.step1_layout.parent_event = lambda *args : None
            self.step1_layout.has_next()
            self.geolocation_step_layout.display_block()
            self.geolocation_step_layout.procced_event = lambda *args : None
            self.geolocation_step_layout.is_not_done = False
            self.fiber_connection_step_layout.display_block()
            self.fiber_connection_step_layout.is_not_done = True
            self.fiber_connection_step_layout.procced_event = self.next_step_3
            self.poc_layout.display_none()
            self.poc_uploader_layout_1.display_none()
            self.poc_uploader_layout_2.display_none()
            self.poc_uploader_layout_3.display_none()
            self.poc_uploader_layout_4.display_none()
            self.poc_uploader_layout_5.display_none()
            self.poc_uploader_layout_6.display_none()
            self.poc_uploader_layout_7.display_none()
            self.poc_uploader_layout_8.display_none()
            self.poc_uploader_layout_9.display_none()
            self.poc_uploader_layout_10.display_none()
            self.poc_uploader_layout_11.display_none()
            self.poc_uploader_layout_12.display_none()
            self.poc_uploader_layout_13.display_none()
            self.poc_uploader_layout_14.display_none()
            self.for_review_layout.display_none()
        elif step == 4:
            self.step1_layout.is_not_done = False
            self.step1_layout.parent_event = lambda *args : None
            self.step1_layout.has_next()
            self.geolocation_step_layout.display_block()
            self.geolocation_step_layout.procced_event = lambda *args : None
            self.geolocation_step_layout.is_not_done = False
            self.fiber_connection_step_layout.display_block()
            self.fiber_connection_step_layout.procced_event = lambda *args : None
            self.fiber_connection_step_layout.is_not_done = False
            self.poc_layout.display_block()
            self.poc_layout.is_not_done = True
            self.poc_uploader_layout_1.display_block()
            self.poc_uploader_layout_1.parent_event = self.update_image_data
            self.poc_uploader_layout_2.display_block()
            self.poc_uploader_layout_2.parent_event = self.update_image_data
            self.poc_uploader_layout_3.display_block()
            self.poc_uploader_layout_3.parent_event = self.update_image_data
            self.poc_uploader_layout_4.display_block()
            self.poc_uploader_layout_4.parent_event = self.update_image_data
            self.poc_uploader_layout_5.display_block()
            self.poc_uploader_layout_5.parent_event = self.update_image_data
            self.poc_uploader_layout_6.display_block()
            self.poc_uploader_layout_6.parent_event = self.update_image_data
            self.poc_uploader_layout_7.display_block()
            self.poc_uploader_layout_7.parent_event = self.update_image_data
            self.poc_uploader_layout_8.display_block()
            self.poc_uploader_layout_8.parent_event = self.update_image_data
            self.poc_uploader_layout_9.display_block()
            self.poc_uploader_layout_9.parent_event = self.update_image_data
            self.poc_uploader_layout_10.display_block()
            self.poc_uploader_layout_10.parent_event = self.update_image_data
            self.poc_uploader_layout_11.display_block()
            self.poc_uploader_layout_11.parent_event = self.update_image_data
            self.poc_uploader_layout_12.display_block()
            self.poc_uploader_layout_12.parent_event = self.update_image_data
            self.poc_uploader_layout_13.display_block()
            self.poc_uploader_layout_13.parent_event = self.update_image_data
            self.poc_uploader_layout_14.display_block()
            self.poc_uploader_layout_14.parent_event = self.update_image_data
            self.for_review_layout.display_block()
            self.for_review_layout.is_not_done = True
            self.for_review_layout.procced_event = self.next_step_4
        elif step == 5:
            self.step1_layout.is_not_done = False
            self.step1_layout.parent_event = lambda *args : None
            self.step1_layout.has_next()
            self.geolocation_step_layout.display_block()
            self.geolocation_step_layout.procced_event = lambda *args : None
            self.geolocation_step_layout.is_not_done = False
            self.fiber_connection_step_layout.display_block()
            self.fiber_connection_step_layout.procced_event = lambda *args : None
            self.fiber_connection_step_layout.is_not_done = False
            self.poc_layout.display_block()
            self.poc_layout.is_not_done = False
            self.poc_uploader_layout_1.display_block()
            self.poc_uploader_layout_1.parent_event = lambda *args : None
            self.poc_uploader_layout_2.display_block()
            self.poc_uploader_layout_2.parent_event = lambda *args : None
            self.poc_uploader_layout_3.display_block()
            self.poc_uploader_layout_3.parent_event = lambda *args : None
            self.poc_uploader_layout_4.display_block()
            self.poc_uploader_layout_4.parent_event = lambda *args : None
            self.poc_uploader_layout_5.display_block()
            self.poc_uploader_layout_5.parent_event = lambda *args : None
            self.poc_uploader_layout_6.display_block()
            self.poc_uploader_layout_6.parent_event = lambda *args : None
            self.poc_uploader_layout_7.display_block()
            self.poc_uploader_layout_7.parent_event = lambda *args : None
            self.poc_uploader_layout_8.display_block()
            self.poc_uploader_layout_8.parent_event = lambda *args : None
            self.poc_uploader_layout_9.display_block()
            self.poc_uploader_layout_9.parent_event = lambda *args : None
            self.poc_uploader_layout_10.display_block()
            self.poc_uploader_layout_10.parent_event = lambda *args : None
            self.poc_uploader_layout_11.display_block()
            self.poc_uploader_layout_11.parent_event = lambda *args : None
            self.poc_uploader_layout_12.display_block()
            self.poc_uploader_layout_12.parent_event = lambda *args : None
            self.poc_uploader_layout_13.display_block()
            self.poc_uploader_layout_13.parent_event = lambda *args : None
            self.poc_uploader_layout_14.display_block()
            self.poc_uploader_layout_14.parent_event = lambda *args : None
            self.for_review_layout.display_block()
            self.for_review_layout.procced_event = lambda *args : None
            self.for_review_layout.is_not_done = False

        


    def next_step_1(self):
        key = "TICKET_NEXT_STEP"
        print("next step 1", key)
        app = MDApp.get_running_app()
        if key in app.communications.key_running:
            return 
        self.manager.proccess_layout.open() 
        app.communications.ticket_next_step({"ticket_id" : self.ticket.get('ticket_id')})
        def communication_event(*args):
            data = app.communications.get_and_remove(key) 
            print("data : ", data)
            if data.get("result", None): 
                self.manager.proccess_layout.display_success(data.get("message"))
                state = data.get( "data", {}).get("state", "N/A")
                self.state_widget.setup(
                    icon_image='alert-circle-check' if state == "Normal" else 'alert-octagram' ,
                    account_info= "Normal" if state == "Normal" else state,
                    color= '#5CBA45' if state == "Normal" else '#B71E1E'
                    )
                
                

                self.has_changed_data = True
                step = data.get("data", {}).get("step", None)
                if step is None:
                    self.go_back()
                else:
                    if step == 1:
                        self.go_back()
                    else:
                        self.display_by_step(step) 
                return False
            elif data.get("result", False) == False: 
                self.manager.proccess_layout.display_error(data.get("message"))
                return False
            elif data.get("result", False) == None:
                self.manager.proccess_layout.display_error(data.get("message"))
                return False
                

        Clock.schedule_interval(communication_event, 1)



    def next_step_2(self, geo_map):
        key = "TICKET_NEXT_STEP"
        print("next step 1", key)
        app = MDApp.get_running_app()
        if key in app.communications.key_running:
            return 
        if geo_map is None: 
            return
        self.manager.proccess_layout.open() 
        app.communications.ticket_next_step({
            "ticket_id" : self.ticket.get('ticket_id'),
            "geo_map" : geo_map
            })
        def communication_event(*args):
            
            data = app.communications.get_and_remove(key) 
            print("data : ", data)
            if data.get("result", None): 
                self.manager.proccess_layout.display_success(data.get("message"))
                self.has_changed_data = True
                state = data.get( "data", {}).get("state", "N/A")
                self.state_widget.setup(
                    icon_image='alert-circle-check' if state == "Normal" else 'alert-octagram' ,
                    account_info= "Normal" if state == "Normal" else state,
                    color= '#5CBA45' if state == "Normal" else '#B71E1E'
                    ) 
                step = data.get("data", {}).get("step", None)
                if step is None:
                    self.go_back()
                else:
                    if step == 2:
                        self.go_back()
                    else:
                        self.display_by_step(step) 
                return False
            elif data.get("result", False) == False: 
                self.manager.proccess_layout.display_error(data.get("message"))
                return False
            elif data.get("result", False) == None:
                self.manager.proccess_layout.display_error(data.get("message"))
                return False
                

        Clock.schedule_interval(communication_event, 1)


    def next_step_3(self, rx , tx):
        key = "TICKET_NEXT_STEP"
        print("next step 1", key)
        app = MDApp.get_running_app()
        if key in app.communications.key_running:
            return 
        if rx is None or tx is None:
            return
        self.manager.proccess_layout.open() 
        app.communications.ticket_next_step({
            "ticket_id" : self.ticket.get('ticket_id'),
            "rx" : rx,
            "tx" : tx
            })
        def communication_event(*args):
            
            data = app.communications.get_and_remove(key) 
            print("data : ", data)
            if data.get("result", None): 
                self.manager.proccess_layout.display_success(data.get("message"))
                self.has_changed_data = True
                state = data.get( "data", {}).get("state", "N/A")
                self.state_widget.setup(
                    icon_image='alert-circle-check' if state == "Normal" else 'alert-octagram' ,
                    account_info= "Normal" if state == "Normal" else state,
                    color= '#5CBA45' if state == "Normal" else '#B71E1E'
                    ) 
                step = data.get("data", {}).get("step", None)
                if step is None:
                    self.go_back()
                else:
                    if step == 3:
                        self.go_back()
                    else:
                        self.display_by_step(step) 
                return False
            elif data.get("result", False) == False: 
                self.manager.proccess_layout.display_error(data.get("message"))
                return False
            elif data.get("result", False) == None:
                self.manager.proccess_layout.display_error(data.get("message"))
                return False
                

        Clock.schedule_interval(communication_event, 1)


    def update_image_data(self):
        
        poc1 = self.poc_uploader_layout_1.selected_images
        if not poc1:
            self.poc_layout.is_not_done = True
            self.for_review_layout.is_ready = False
            return
        
        poc2 = self.poc_uploader_layout_2.selected_images
        if not poc2:
            self.poc_layout.is_not_done = True
            self.for_review_layout.is_ready = False
            return

        poc3 = self.poc_uploader_layout_3.selected_images
        if not poc3:
            self.poc_layout.is_not_done = True
            self.for_review_layout.is_ready = False
            return
        
        poc4 = self.poc_uploader_layout_4.selected_images
        if not poc4:
            self.poc_layout.is_not_done = True
            self.for_review_layout.is_ready = False
            return
        
        poc5 = self.poc_uploader_layout_5.selected_images
        if not poc5:
            self.poc_layout.is_not_done = True
            self.for_review_layout.is_ready = False
            return
        
        poc6 = self.poc_uploader_layout_6.selected_images
        if not poc6:
            self.poc_layout.is_not_done = True
            self.for_review_layout.is_ready = False
            return
        
        poc7 = self.poc_uploader_layout_7.selected_images
        if not poc7:
            self.poc_layout.is_not_done = True
            self.for_review_layout.is_ready = False
            return
        
        poc8 = self.poc_uploader_layout_8.selected_images
        if not poc8:
            self.poc_layout.is_not_done = True
            self.for_review_layout.is_ready = False
            return
        

        poc9 = self.poc_uploader_layout_9.selected_images
        if not poc9:
            self.poc_layout.is_not_done = True
            self.for_review_layout.is_ready = False
            return
        

        poc10 = self.poc_uploader_layout_10.selected_images
        if not poc10:
            self.poc_layout.is_not_done = True
            self.for_review_layout.is_ready = False
            return

        poc11 = self.poc_uploader_layout_11.selected_images
        if not poc11:
            self.poc_layout.is_not_done = True
            self.for_review_layout.is_ready = False
            return

        poc12 = self.poc_uploader_layout_12.selected_images
        if not poc12:
            self.poc_layout.is_not_done = True
            self.for_review_layout.is_ready = False
            return

        poc13 = self.poc_uploader_layout_13.selected_images
        if not poc13:
            self.poc_layout.is_not_done = True
            self.for_review_layout.is_ready = False
            return

        poc14 = self.poc_uploader_layout_14.selected_images
        if not poc14:
            self.poc_layout.is_not_done = True
            self.for_review_layout.is_ready = False
            return 
 
        self.images_data = {
            "poc1" : poc1,
            "poc2" : poc2,
            "poc3" : poc3,
            "poc4" : poc4,
            "poc5" : poc5,
            "poc6" : poc6,
            "poc7" : poc7,
            "poc8" : poc8,
            "poc9" : poc9,
            "poc10" : poc10,
            "poc11" : poc11,
            "poc12" : poc12,
            "poc13" : poc13,
            "poc14" : poc14
        }
        self.poc_layout.is_not_done = False
        self.for_review_layout.is_ready = True


    def next_step_4(self):
        key = "TICKET_NEXT_STEP"
        print("next step 1", key)
        app = MDApp.get_running_app()
        if key in app.communications.key_running:
            return  
        if not self.images_data:
            return
        
        self.manager.proccess_layout.open()
        proccess_data = {
            "ticket_id" : self.ticket.get('ticket_id')
        }
        poc_keys = {
            'poc1' : 'customer_signature',
            'poc2' : 'terminal_box',
            'poc3' : 'terminal_box_tag',
            'poc4' : 'modem_serial',
            'poc5' : 'modem_setup',
            'poc6' : 'configuration',
            'poc7' : 'rx_tx',
            'poc8' : 'signal_pon',
            'poc9' : 'speedtest_2g',
            'poc10' : 'speedtest_5g',
            'poc11' : 'wifi_analyzer_2g',
            'poc12' : 'wifi_analyzer_5g',
            'poc13' : 'geolocation',
            'poc14' : 'ticket_form'
        } 

        for imkey in self.images_data:
            proccess_data[poc_keys[imkey]] = []
            for innerimkey in self.images_data[imkey]:
                converted_imagepath = image_path_to_base64(self.images_data[imkey][innerimkey])
                proccess_data[poc_keys[imkey]].append(converted_imagepath)

        app.communications.ticket_next_step(proccess_data)
        def communication_event(*args):
            
            data = app.communications.get_and_remove(key) 
            print("data : ", data)
            if data.get("result", None): 
                self.manager.proccess_layout.display_success(data.get("message"))
                self.has_changed_data = True
                state = data.get( "data", {}).get("state", "N/A")
                self.state_widget.setup(
                    icon_image='alert-circle-check' if state == "Normal" else 'alert-octagram' ,
                    account_info= "Normal" if state == "Normal" else state,
                    color= '#5CBA45' if state == "Normal" else '#B71E1E'
                    ) 
                step = data.get("data", {}).get("step", None)
                if step is None:
                    self.go_back()
                else:
                    if step == 4:
                        self.go_back()
                    else:
                        self.display_by_step(step) 
                return False
            elif data.get("result", False) == False: 
                self.manager.proccess_layout.display_error(data.get("message"))
                return False
            elif data.get("result", False) == None:
                self.manager.proccess_layout.display_error(data.get("message"))
                return False
                

        Clock.schedule_interval(communication_event, 1)



    def refetch_remarks(self, *args):
        key = "REFETCH_REMARKS" 
        app = MDApp.get_running_app()
        if key in app.communications.key_running:
            return 
        app.communications.refetch_remarks( self.ticket.get('ticket_id') )
        def communication_event(*args):
            data = app.communications.get_and_remove(key)  
            if data.get("result", None):
                remarks = data.get("data", {}).get("remarks", [])
                self.remarks_list.add_remarks_from_list(remarks)
                return False
            elif data.get("result", False) == False: 
                return False
            elif data.get("result", False) == None:
                return False
                

        Clock.schedule_interval(communication_event, 1)
    






