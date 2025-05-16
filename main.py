from kivy.uix.accordion import ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivy.lang.builder import Builder
from kivy.core.text import LabelBase
from kivy.utils import platform, get_color_from_hex

from variables import *
from login import main_login_screen  # Import login screen class
import os
import json

from kivy.config import Config
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.modalview import ModalView
from kivy.uix.image import Image

from communications  import Communications
from kivy.logger import Logger

if platform == "android": 
    from android.permissions import request_permissions, Permission, check_permission  # pylint: disable=import-error

if platform == "ios":
    pass

from kivy.core.window import Window
Window.show_cursor = True


# Set Window Size Before App Starts if platform is 
if platform == "win":
    Window.size = (320, 568)


class MainApp(MDScreenManager):  # Acts as ScreenManager
    pass

class TappableImage(Image):
    def __init__(self, modal_ref, **kwargs):
        super().__init__(**kwargs)
        self.modal_ref = modal_ref

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.modal_ref.dismiss()
            return True
        return super().on_touch_down(touch)


class ImageModal(ModalView):
    def __init__(self, image_path, **kwargs):
        super().__init__(**kwargs)
        self.auto_dismiss = False  # Don't dismiss by tapping outside
        self.background_color = (0, 0, 0, 0)
        self.image_widget = TappableImage(
            source=image_path,
            allow_stretch=True,
            keep_ratio=True,
            modal_ref=self
        )
        self.add_widget(self.image_widget)


class TechnicalApp(MDApp): 
    
    user_app_data : dict = None
    communications : Communications = None
    done_load_modal : ImageModal = ObjectProperty(None)
    
    def on_start(self):
        """ Check and request storage permission on Android """

        if platform == "android":
            if self.check_permissions():
                # print("✅ Storage permission already granted.")
                pass
            else:
                # print("❌ Storage permission NOT granted. Requesting now...")
                request_permissions([
                    Permission.INTERNET,
                    Permission.ACCESS_FINE_LOCATION,
                    Permission.ACCESS_COARSE_LOCATION,
                    Permission.READ_MEDIA_IMAGES,
                    Permission.READ_MEDIA_VIDEO,
                    Permission.READ_MEDIA_AUDIO,
                    Permission.READ_EXTERNAL_STORAGE,
                    Permission.WRITE_EXTERNAL_STORAGE,
                ])
        # Defer screen loading after UI is visible
        Clock.schedule_once(self.load_screens, 0.1)

    def check_permissions(self):
        """ Check if READ/WRITE storage permissions are granted """
        if platform == "android":
            perms = [
                Permission.INTERNET,
                Permission.ACCESS_FINE_LOCATION,
                Permission.ACCESS_COARSE_LOCATION,
                Permission.READ_MEDIA_IMAGES,
                Permission.READ_MEDIA_VIDEO,
                Permission.READ_MEDIA_AUDIO,
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE,
            ] 
            return all(check_permission(p) for p in perms)
        return True  # ✅ Assume granted on other platforms
    

    def on_stop(self):
        try:
            # Save user app data
            with open("user_data.json", "w") as f:
                json.dump(self.user_app_data, f)
            # Close communications
            self.communications.kill_all_threads()
        except Exception as e:
            # print(f"Error saving user data: {e}")
            pass

    def on_pause(self):
        Clock.schedule_once(self.show_welcome_popup, 0.1)
        # Save user app data
        try:
            with open("user_data.json", "w") as f:
                json.dump(self.user_app_data, f)
        except Exception as e:
            # print(f"Error saving user data: {e}")
            pass
        return super().on_pause()

            
    def build(self):
        
        self.theme_cls.primary_dark = get_color_from_hex("#F7EEDD")
        
        # Get user app data
        try:
            with open("user_data.json", "r") as f:
                self.user_app_data = json.load(f)
        except:
            self.user_app_data = {
                "username": None,
                "password": None
            }
        
        # Set App Icon
        self.icon = os.path.join(os.path.dirname(__file__), 'assets', 'app_logo.png')
        splash_image = os.path.join(os.path.dirname(__file__), 'assets', 'splash_app.png')

        self.done_load_modal = ImageModal(splash_image)

        
        # Set App Communications
        self.communications = Communications()
        # Load Application 
        Builder.load_file('main.kv')  # ✅ Load only UI, not screens
        sm = MainApp()
        self.root_screen_manager = sm

        
        # Load login screen
        login_component_kv_path = os.path.join(os.path.dirname(__file__), 'login', "login_design.kv")
        login_kv_path = os.path.join(os.path.dirname(__file__), 'login', "main_login_screen.kv") 
        login_pin_kv_path = os.path.join(os.path.dirname(__file__), 'login', "pinlogin.kv")
        register_account_kv_path = os.path.join(os.path.dirname(__file__), 'login', "registeraccount.kv")
        register_pin_kv_path = os.path.join(os.path.dirname(__file__), 'login', "registerpin.kv")
        Builder.load_file(login_component_kv_path)
        Builder.load_file(login_kv_path)
        Builder.load_file(login_pin_kv_path)
        Builder.load_file(register_account_kv_path)
        Builder.load_file(register_pin_kv_path)
        
        login_screen = main_login_screen.LoginScreen(name=LOGIN_SCREEN)
        self.root_screen_manager.add_widget(login_screen)  # ✅ Add screens via Python
        def change_to_login_screen(*args):
            print("this happen hehehee")
            self.root_screen_manager.current = LOGIN_SCREEN
        Clock.schedule_once(self.show_welcome_popup, 0.5)
        Clock.schedule_once(change_to_login_screen, 1) 

        return sm
        

    def show_welcome_popup(self, *args):
        self.done_load_modal.open()
        def close_popup(*args):
            self.done_load_modal.dismiss()
        Clock.schedule_once(close_popup, 1)

    
    def load_screens(self, *args):

        # # Load login screen
        # login_component_kv_path = os.path.join(os.path.dirname(__file__), 'login', "login_design.kv")
        # login_kv_path = os.path.join(os.path.dirname(__file__), 'login', "main_login_screen.kv") 
        # login_pin_kv_path = os.path.join(os.path.dirname(__file__), 'login', "pinlogin.kv")
        # register_account_kv_path = os.path.join(os.path.dirname(__file__), 'login', "registeraccount.kv")
        # register_pin_kv_path = os.path.join(os.path.dirname(__file__), 'login', "registerpin.kv")
        # Builder.load_file(login_component_kv_path)
        # Builder.load_file(login_kv_path)
        # Builder.load_file(login_pin_kv_path)
        # Builder.load_file(register_account_kv_path)
        # Builder.load_file(register_pin_kv_path)
        

        # Load home screen
        account_kv_path = os.path.join(os.path.dirname(__file__), 'home', 'account.kv')
        dashboard_kv_path = os.path.join(os.path.dirname(__file__), 'home', 'dashboard.kv')
        home_component_kv_path = os.path.join(os.path.dirname(__file__), 'home', 'home_component.kv')
        ticket_transaction_kv_path = os.path.join(os.path.dirname(__file__), 'home', 'ticket_transact.kv')
        ticket_list_kv_path = os.path.join(os.path.dirname(__file__), 'home', 'ticket_list.kv')    
        home_kv_path = os.path.join(os.path.dirname(__file__), 'home', 'home.kv')
        
        Builder.load_file(dashboard_kv_path)
        Builder.load_file(home_component_kv_path)   
        Builder.load_file(ticket_transaction_kv_path)
        Builder.load_file(ticket_list_kv_path) 
        Builder.load_file(home_kv_path)
        Builder.load_file(account_kv_path)

if __name__ == '__main__':
    LabelBase.register(name="roboto_extrabolditalic", fn_regular=os.path.join(os.path.dirname(__file__), 'fonts', 'Roboto-ExtraBoldItalic.ttf'))
    LabelBase.register(name="roboto_extralightitalic", fn_regular=os.path.join(os.path.dirname(__file__), 'fonts', 'Roboto-ExtraLightItalic.ttf'))
    LabelBase.register(name="roboto_extralight", fn_regular=os.path.join(os.path.dirname(__file__), 'fonts', 'Roboto-ExtraLight.ttf'))
    LabelBase.register(name="roboto_semibold", fn_regular=os.path.join(os.path.dirname(__file__), 'fonts', 'Roboto-SemiBold.ttf'))
    LabelBase.register(name="roboto_extrabold", fn_regular=os.path.join(os.path.dirname(__file__), 'fonts', 'Roboto-ExtraBold.ttf'))
    LabelBase.register(name="roboto_light", fn_regular=os.path.join(os.path.dirname(__file__), 'fonts', 'Roboto-Light.ttf'))
    LabelBase.register(name="roboto_lightitalic", fn_regular=os.path.join(os.path.dirname(__file__), 'fonts', 'Roboto-LightItalic.ttf'))
    try:
        TechnicalApp().run()
    except KeyboardInterrupt:
        print("KeyboardInterrupt detected. Exiting...")
    except Exception as e:
        print(f"Error: {e}")
    
