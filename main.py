from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivy.lang.builder import Builder
from kivy.core.text import LabelBase
from kivy.utils import platform, get_color_from_hex

from variables import *
from login import main_login_screen  # Import login screen class
from home import home
import os
import json

from kivy.config import Config
from kivy.core.window import Window

if platform == "android":
    from plyer.platforms.android.sms import Sms
    from android.permissions import request_permissions, Permission, check_permission  # pylint: disable=import-error


# Set Window Size Before App Starts
Window.size = (320, 568)




class MainApp(MDScreenManager):  # Acts as ScreenManager
    pass

class TechnicalApp(MDApp): 
    
    user_app_data : dict = None
    
    def on_start(self):
        """ Check and request storage permission on Android """
        if platform == "android":
            if self.check_permissions():
                print("✅ Storage permission already granted.")
            else:
                print("❌ Storage permission NOT granted. Requesting now...")
                request_permissions([
                    Permission.READ_EXTERNAL_STORAGE,
                    Permission.WRITE_EXTERNAL_STORAGE,
                    Permission.ACCESS_FINE_LOCATION,  # ✅ GPS Permission
                    Permission.ACCESS_COARSE_LOCATION  # ✅ Coarse GPS Permission
                ])

    def check_permissions(self):
        """ Check if READ/WRITE storage permissions are granted """
        if platform == "android":
            has_read = check_permission(Permission.READ_EXTERNAL_STORAGE)
            has_write = check_permission(Permission.WRITE_EXTERNAL_STORAGE)
            return has_read and has_write
        return True  # ✅ Assume granted on other platforms

            
    def build(self):
        
        self.theme_cls.primary_dark = get_color_from_hex("#F7EEDD")
        
        # Get user app data
        try:
            with open("user_data.json", "r") as f:
                self.user_app_data = json.load(f)
        except:
            self.user_app_data = {}
        
        # Set App Icon
        self.icon = os.path.join(os.path.dirname(__file__), 'assets', 'app_logo.png')
        
        # Load Application 
        Builder.load_file('main.kv')  # ✅ Load only UI, not screens
        self.root_screen_manager = MainApp()  # ✅ Initialize empty ScreenManager
        
        
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
        
        # Load home screen
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
        
        home_screen = home.HomeScreen(name=HOME_SCREEN)
        self.root_screen_manager.add_widget(home_screen)  # ✅ Add screens via Python
        self.root_screen_manager.current = HOME_SCREEN
        
        
        
        return self.root_screen_manager

if __name__ == '__main__':
    LabelBase.register(name="roboto_extrabolditalic", fn_regular=os.path.join(os.path.dirname(__file__), 'fonts', 'Roboto-ExtraBoldItalic.ttf'))
    LabelBase.register(name="roboto_extralightitalic", fn_regular=os.path.join(os.path.dirname(__file__), 'fonts', 'Roboto-ExtraLightItalic.ttf'))
    LabelBase.register(name="roboto_extralight", fn_regular=os.path.join(os.path.dirname(__file__), 'fonts', 'Roboto-ExtraLight.ttf'))
    LabelBase.register(name="roboto_semibold", fn_regular=os.path.join(os.path.dirname(__file__), 'fonts', 'Roboto-SemiBold.ttf'))
    LabelBase.register(name="roboto_extrabold", fn_regular=os.path.join(os.path.dirname(__file__), 'fonts', 'Roboto-ExtraBold.ttf'))
    LabelBase.register(name="roboto_light", fn_regular=os.path.join(os.path.dirname(__file__), 'fonts', 'Roboto-Light.ttf'))
    LabelBase.register(name="roboto_lightitalic", fn_regular=os.path.join(os.path.dirname(__file__), 'fonts', 'Roboto-LightItalic.ttf'))
    TechnicalApp().run()
