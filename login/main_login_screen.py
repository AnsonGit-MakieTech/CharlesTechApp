
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, NumericProperty, StringProperty 
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout 
from kivy.animation import Animation
from kivy.uix.button import Button
from kivy.uix.image import Image
from types import MethodType  # ✅ Import MethodType
from kivy.clock import Clock
from kivy.utils import platform
from kivy.uix.screenmanager import SlideTransition, FadeTransition, SwapTransition, ScreenManager
from kivymd.app import MDApp



import os
from utils import *

from .login_components import *
from variables import *
from utils.app_utils import *




class RegisterPinScreen(Screen):
    circle_size = NumericProperty(min(Window.width * 0.9, Window.height * 0.5))
    go_back_screen_font_size = NumericProperty(0)  # ✅ Initialize with 0 (Will update later)
    title_font_size = NumericProperty(0)  # ✅ Initialize with 0 (Will update later)
    text_input_font_size = NumericProperty(0)
    pin_info_font_size = NumericProperty(0)
    
    back_image: Image = ObjectProperty(None)
    back_text: Button = ObjectProperty(None)
    
    keyboard_open = False  # ✅ Track if keyboard is open
    move_y = NumericProperty(0)  # ✅ Track screen shift
 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.update_size()  # Set initial size
        Window.bind(size=self.update_size)  # Bind window resize event
        
        if platform == 'android':
            self.trigger_keyboard_height = Clock.create_trigger(self.update_keyboard_height, 0.2, interval=True)
            self.trigger_cancel_keyboard_height = Clock.create_trigger(lambda dt: self.trigger_keyboard_height.cancel(), 1.0, interval=False)

    
    def update_keyboard_height(self, dt):
        """ Detect keyboard height and move screen if necessary """
        if platform == 'android':
            keyboard_height = get_android_keyboard_height()
            if keyboard_height > 0:  # ✅ Keyboard is opened
                if not self.keyboard_open:
                    self.keyboard_open = True
                    Animation(move_y=keyboard_height / Window.height, d=0.2).start(self)
            else:  # ✅ Keyboard is closed
                if self.keyboard_open:
                    self.keyboard_open = False
                    Animation(move_y=0, d=0.2).start(self)
    
    def _bind_keyboard(self):
        """ Bind keyboard event to start checking """
        super()._bind_keyboard()
        if platform == 'android':
            self.trigger_cancel_keyboard_height.cancel()
            self.trigger_keyboard_height()
    
    def _unbind_keyboard(self):
        """ Unbind keyboard event when done """
        super()._unbind_keyboard()
        if platform == 'android':
            self.trigger_cancel_keyboard_height()

    def on_enter(self, *args):
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

        
    def update_size(self, *args):
        """ Update circle size dynamically when window size changes """
        self.circle_size = min(Window.width * 0.9, Window.height * 0.5)
        self.go_back_screen_font_size = min(Window.width, Window.height) * 0.02
        self.title_font_size = min(Window.width, Window.height) * 0.025
        self.text_input_font_size = min(Window.width, Window.height) * 0.02
        self.pin_info_font_size = min(Window.width, Window.height) * 0.018

    def go_back(self, *args): 
        if self.manager.parent.user_screen_action == LOGIN_SCREEN_ACTION_REGISTER:
            self.manager.transition.direction = 'right'
        else:
            self.manager.transition.direction = 'left'
        self.manager.current =  LOGIN_SCREEN_REGISTER_ACCOUNT_SCREEN







class RegisterAccountScreen(Screen):
    circle_size = NumericProperty(min(Window.width * 0.9, Window.height * 0.5))
    go_back_screen_font_size = NumericProperty(0)  # ✅ Initialize with 0 (Will update later)
    title_font_size = NumericProperty(0)  # ✅ Initialize with 0 (Will update later)
    text_input_font_size = NumericProperty(0)
    back_image: Image = ObjectProperty(None)
    back_text: Button = ObjectProperty(None)
    login_button_text : str = StringProperty('')
    
    keyboard_open = False  # ✅ Track if keyboard is open
    move_y = NumericProperty(0)  # ✅ Track screen shift
 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.update_size()  # Set initial size
        Window.bind(size=self.update_size)  # Bind window resize event
        
        if platform == 'android':
            self.trigger_keyboard_height = Clock.create_trigger(self.update_keyboard_height, 0.2, interval=True)
            self.trigger_cancel_keyboard_height = Clock.create_trigger(lambda dt: self.trigger_keyboard_height.cancel(), 1.0, interval=False)

    
    def update_keyboard_height(self, dt):
        """ Detect keyboard height and move screen if necessary """
        if platform == 'android':
            keyboard_height = get_android_keyboard_height()
            if keyboard_height > 0:  # ✅ Keyboard is opened
                if not self.keyboard_open:
                    self.keyboard_open = True
                    Animation(move_y=keyboard_height / Window.height, d=0.2).start(self)
            else:  # ✅ Keyboard is closed
                if self.keyboard_open:
                    self.keyboard_open = False
                    Animation(move_y=0, d=0.2).start(self)
    
    def _bind_keyboard(self):
        """ Bind keyboard event to start checking """
        super()._bind_keyboard()
        if platform == 'android':
            self.trigger_cancel_keyboard_height.cancel()
            self.trigger_keyboard_height()
    
    def _unbind_keyboard(self):
        """ Unbind keyboard event when done """
        super()._unbind_keyboard()
        if platform == 'android':
            self.trigger_cancel_keyboard_height()

    def on_enter(self, *args):
        self.back_text.on_press=self.go_back
        if self.manager.parent.user_screen_action == LOGIN_SCREEN_ACTION_REGISTER:
            self.login_button_text = 'Register'
        else:
            self.login_button_text = 'Update'
            
        def on_touch_down(image, touch):
            """ Detect touch inside the image """
            if image.collide_point(*touch.pos):
                self.go_back()
                return True  # ✅ Stops event propagation if needed
            return super(image.__class__, image).on_touch_down(touch)  # ✅ Call original method

        # ✅ Bind on_touch_down correctly
        self.back_image.on_touch_down = MethodType(on_touch_down, self.back_image)
        
        return super().on_enter(*args)

        
    def update_size(self, *args):
        """ Update circle size dynamically when window size changes """
        self.circle_size = min(Window.width * 0.9, Window.height * 0.5)
        self.go_back_screen_font_size = min(Window.width, Window.height) * 0.02
        self.title_font_size = min(Window.width, Window.height) * 0.03
        self.text_input_font_size = min(Window.width, Window.height) * 0.025

    def go_back(self, *args): 
        if self.manager.parent.user_screen_action == LOGIN_SCREEN_ACTION_REGISTER:
            self.manager.transition.direction = 'right'
        else:
            self.manager.transition.direction = 'left'
            
        self.manager.current = LOGIN_SCREEN_PIN_LOGIN_SCREEN

    def register_account(self, *args):
        if self.manager.parent.user_screen_action == LOGIN_SCREEN_ACTION_REGISTER: 
            self.manager.transition.direction = 'left'
        else:
            self.manager.transition.direction = 'right'
        
        self.manager.current = LOGIN_SCREEN_REGISTER_PIN_SCREEN



class PinHolder(BoxLayout):
    pin1 : PinWidget = ObjectProperty(None)
    pin2 : PinWidget = ObjectProperty(None)
    pin3 : PinWidget = ObjectProperty(None)
    pin4 : PinWidget = ObjectProperty(None)
    
    def reset(self):
        self.pin1.toggle()
        self.pin2.toggle()
        self.pin3.toggle()
        self.pin4.toggle()
        
    def shake(self):
        """ Animate a left-right shaking effect """
        shake_distance = 10  # How far the button moves left/right
        shake_speed = 0.05  # Speed of each movement

        anim1 = Animation(x=self.x - shake_distance, duration=shake_speed)
        anim2 = Animation(x=self.x + shake_distance * 2, duration=shake_speed)
        anim3 = Animation(x=self.x - shake_distance, duration=shake_speed)
        anim4 = Animation(x=self.x, duration=shake_speed)  # Reset position

        shake_anim = anim1 + anim2 + anim3 + anim4  # Chain animations
        shake_anim.repeat = False  # Make sure it does not loop forever
        shake_anim.start(self)

class PinKeyboard(BoxLayout):
    log_pin : str = StringProperty('')
    
    def input(self, pin : str):
        self.log_pin += pin
        print(self.log_pin)
        if len(self.log_pin) == 1:
            self.parent.parent.parent.pinholder.pin1.toggle()
        if len(self.log_pin) == 2:
            self.parent.parent.parent.pinholder.pin2.toggle()
        if len(self.log_pin) == 3:
            self.parent.parent.parent.pinholder.pin3.toggle()
        if len(self.log_pin) == 4:
            self.parent.parent.parent.pinholder.pin4.toggle()
            
        if len(self.log_pin) == 4:
            self.validate_pin()
            
    def validate_pin(self):
        print('validate_pin : ', self.log_pin)
        app = MDApp.get_running_app()
        user_data = app.user_app_data
        if user_data.get('pin', None) != self.log_pin: 
            self.parent.parent.parent.pinholder.shake()
            self.parent.parent.parent.pinholder.reset()
            self.log_pin = '' 
            return
            
        self.parent.parent.parent.manager.parent.manager.current = HOME_SCREEN
        self.log_pin = ''

class PinLoginScreen(Screen):
    circle_size = NumericProperty(min(Window.width * 0.9, Window.height * 0.5))
    never_forget_pin_font_size = NumericProperty(0)
    
    pinholder : PinHolder = ObjectProperty(None)
    
    forgot_pin:  ClickableLabel = ObjectProperty(None)
    register_pin:  ClickableLabel = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_size()  # Set initial size
        Window.bind(size=self.update_size)  # Bind window resize event

        self.forgot_pin.label_event = self.forgot_pin_event
        self.register_pin.label_event = self.register_pin_event
        
    
    def on_enter(self, *args):
        self.manager.parent.user_screen_action = LOGIN_SCREEN_ACTION_PIN
        return super().on_enter(*args)

    def forgot_pin_event(self): 
        
        print('forgot_pin') 
        self.manager.parent.user_screen_action = LOGIN_SCREEN_ACTION_FORGOT_PIN
        self.manager.transition.direction = 'right'
        self.manager.current = LOGIN_SCREEN_REGISTER_ACCOUNT_SCREEN
        
    def register_pin_event(self):
        print('register_pin') 
        self.manager.parent.user_screen_action = LOGIN_SCREEN_ACTION_REGISTER
        self.manager.transition.direction = 'left'
        self.manager.current = LOGIN_SCREEN_REGISTER_ACCOUNT_SCREEN

    def update_size(self, *args):
        """ Update circle size dynamically when window size changes """
        self.circle_size = min(Window.width * 0.9, Window.height * 0.5)
        self.never_forget_pin_font_size = min(Window.width, Window.height) * 0.02
        


class LoginScreenManager(ScreenManager):
    
    go_back_icon : str = StringProperty('')
    popup : ProcessingModal = ObjectProperty(None)
    custom_popup : ControllableModal = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        parent_dir = os.path.dirname(os.path.dirname(__file__)) 
        
        self.go_back_icon = os.path.join(parent_dir, 'assets', 'go_back_icon.png')
        print(self.go_back_icon)
        
        self.popup = ProcessingModal()
        self.custom_popup = ControllableModal()
        
        # Clock.schedule_once(self.custom_popup.open, 3)


class LoginScreen(Screen):
    
    login_screen_manager : LoginScreenManager = None
    user_screen_action : str = StringProperty('')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        """ Load KV file only when the screen is about to be entered """
        
        # Access the app instance
        app = MDApp.get_running_app()
        user_data = app.user_app_data
        
        print("App Data : ", app.user_app_data)
            
        if self.login_screen_manager is None:
            self.login_screen_manager = LoginScreenManager(transition=SlideTransition(duration=0.1)) 
            
            self.add_widget(self.login_screen_manager)
        
            pinlogin = PinLoginScreen(name=LOGIN_SCREEN_PIN_LOGIN_SCREEN) 
            # self.login_screen_manager.current = LOGIN_SCREEN_PIN_LOGIN_SCREEN  
            print(self.login_screen_manager.current)
            
            register_account = RegisterAccountScreen(name=LOGIN_SCREEN_REGISTER_ACCOUNT_SCREEN)
            # self.login_screen_manager.current = LOGIN_SCREEN_REGISTER_ACCOUNT_SCREEN
            print(self.login_screen_manager.current)
            
            register_pin = RegisterPinScreen(name=LOGIN_SCREEN_REGISTER_PIN_SCREEN)
            # self.login_screen_manager.current = LOGIN_SCREEN_REGISTER_PIN_SCREEN
            print(self.login_screen_manager.current)

            
            if user_data.get('pin', None) is not None:
                # User has a PIN, show the PIN login screen
                self.login_screen_manager.add_widget(pinlogin)
                self.login_screen_manager.add_widget(register_account)
            else:
                # User does not have a PIN, show the register account screen
                self.user_screen_action = LOGIN_SCREEN_ACTION_REGISTER
                self.login_screen_manager.add_widget(register_account)
                self.login_screen_manager.add_widget(pinlogin)
                
            self.login_screen_manager.add_widget(register_pin)


