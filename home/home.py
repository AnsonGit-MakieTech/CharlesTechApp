
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager
from kivy.animation import Animation
from kivymd.uix.button import MDIconButton
from kivy.utils import get_color_from_hex  # Convert hex colors
from kivy.metrics import dp, sp  # For size scaling
from kivy.clock import Clock

from variables import *
from .ticket_list import TicketListScreen


class HomeScreenManager(ScreenManager):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        home = Screen(name=HOME_SCREEN_DASHBOARD_SCREEN)
        self.add_widget(home)
        
        ticket_list = TicketListScreen(name=HOME_SCREEN_TICKETLIST_SCREEN)
        self.add_widget(ticket_list)
        
        account = Screen(name=HOME_SCREEN_ACCOUNT_SCREEN)
        self.add_widget(account)


class NavigationBar(BoxLayout):
    
    dashboard_button : MDIconButton = ObjectProperty(None)
    ticket_button : MDIconButton = ObjectProperty(None)
    settings_button : MDIconButton = ObjectProperty(None)
    
    anim_button : Animation = None
    anim_button_selected : Animation = None
    maximum_icon_font_size = 35
    minimum_icon_font_size = 23
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.anim_button_selected = Animation(
            font_size = sp(self.maximum_icon_font_size),
            color = get_color_from_hex("#FFFFFF"),
            duration=0.3
        )
        self.anim_button = Animation(
            font_size= sp(self.minimum_icon_font_size),
            color = get_color_from_hex("#ACE2E1"),
            duration=0.3
        )
    
    def setup_butttons(self):
        self.anim_button_selected.start(self.dashboard_button)
        self.anim_button.start(self.ticket_button)
        self.anim_button.start(self.settings_button)
        self.dashboard_button.bind(on_press = self.on_dashboard_button_release)
        self.ticket_button.bind(on_press = self.on_ticket_button_release)
        self.settings_button.bind(on_press = self.on_settings_button_release)
        
        
    def on_dashboard_button_release(self, *args):
        # self.user_screen_action = 'dashboard'
        if self.dashboard_button.font_size <= sp(self.minimum_icon_font_size):
            self.anim_button_selected.start(self.dashboard_button)
        if self.ticket_button.font_size >= sp(self.maximum_icon_font_size):
            self.anim_button.start(self.ticket_button)
        if self.settings_button.font_size >= sp(self.maximum_icon_font_size):
            self.anim_button.start(self.settings_button)
        print(f'Button selected : {HOME_SCREEN_DASHBOARD_SCREEN}')
        self.parent.parent.home_screen_manager.current = HOME_SCREEN_DASHBOARD_SCREEN
    
    def on_ticket_button_release(self, *args):
        # self.user_screen_action = 'ticket'
        if self.dashboard_button.font_size >= sp(self.maximum_icon_font_size):
            self.anim_button.start(self.dashboard_button)
        if self.ticket_button.font_size <= sp(self.minimum_icon_font_size):
            self.anim_button_selected.start(self.ticket_button)
        if self.settings_button.font_size >= sp(self.maximum_icon_font_size):
            self.anim_button.start(self.settings_button)
        print(f'Button selected : {HOME_SCREEN_TICKETLIST_SCREEN}') 
        self.parent.parent.home_screen_manager.current = HOME_SCREEN_TICKETLIST_SCREEN
        
        
    
    def on_settings_button_release(self, *args):
        # self.user_screen_action = 'settings'
        if self.dashboard_button.font_size >= sp(self.maximum_icon_font_size):
            self.anim_button.start(self.dashboard_button)
        if self.ticket_button.font_size >= sp(self.maximum_icon_font_size):
            self.anim_button.start(self.ticket_button)
        if self.settings_button.font_size <= sp(self.minimum_icon_font_size):
            self.anim_button_selected.start(self.settings_button) 
        print(f'Button selected : {HOME_SCREEN_ACCOUNT_SCREEN}') 
        self.parent.parent.home_screen_manager.current = HOME_SCREEN_ACCOUNT_SCREEN
    

class HomeScreen(Screen):
    
    # login_screen_manager : LoginScreenManager = None
    user_screen_action : str = StringProperty('dashboard')
    navigation_bar : NavigationBar = ObjectProperty(None)
    home_screen_manager : HomeScreenManager = ObjectProperty(None)

    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
         
        
         

    
    def on_pre_enter(self, *args):
        self.navigation_bar.setup_butttons()
        return super().on_pre_enter(*args)
    
    
            
            
            
            