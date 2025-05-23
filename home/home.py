
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.animation import Animation
from kivymd.uix.button import MDIconButton
from kivy.utils import get_color_from_hex  # Convert hex colors
from kivy.metrics import dp, sp  # For size scaling
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout

from variables import *
from .dashboard import Dashboard, MemberDataWidget
from .ticket_list import TicketListScreen
from .ticket_transact import TicketTransactionScreeen
from .home_component import ProcessingLayout
from .account import AccountScreen

from kivymd.app import MDApp

class HomeScreenManager(ScreenManager):
     
    proccess_layout : ProcessingLayout = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.proccess_layout = ProcessingLayout()
        
        self.transition = SlideTransition(duration=0.3)  # ✅ Set here!

        home = Dashboard(name=HOME_SCREEN_DASHBOARD_SCREEN)
        self.add_widget(home)

        ticket_list = TicketListScreen(name=HOME_SCREEN_TICKETLIST_SCREEN)
        self.add_widget(ticket_list)

        account = AccountScreen(name=HOME_SCREEN_ACCOUNT_SCREEN)
        self.add_widget(account)
        
        transact = TicketTransactionScreeen(name=HOME_SCREEN_TRANSACT_SCREEN)
        self.add_widget(transact)
    


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
        if self.parent.home_screen_manager.current == HOME_SCREEN_TRANSACT_SCREEN:
            return
        
        # self.user_screen_action = 'dashboard'
        if self.dashboard_button.font_size <= sp(self.minimum_icon_font_size):
            self.anim_button_selected.start(self.dashboard_button)
        if self.ticket_button.font_size >= sp(self.maximum_icon_font_size):
            self.anim_button.start(self.ticket_button)
        if self.settings_button.font_size >= sp(self.maximum_icon_font_size):
            self.anim_button.start(self.settings_button)
        # print(f'Button selected : {HOME_SCREEN_DASHBOARD_SCREEN}')
        # if hasattr(self.parent.home_screen_manager, 'transition') and self.parent.home_screen_manager.transition:
        #     # print("✅ ScreenManager has a transition set:", self.parent.home_screen_manager.transition)
        # else:
        #     # print("❌ No transition set")

        self.parent.home_screen_manager.transition.direction = 'left'
        self.parent.home_screen_manager.current = HOME_SCREEN_DASHBOARD_SCREEN
        

    
    def on_ticket_button_release(self, *args):
        if self.parent.home_screen_manager.current == HOME_SCREEN_TRANSACT_SCREEN:
            return
        # self.user_screen_action = 'ticket'
        if self.dashboard_button.font_size >= sp(self.maximum_icon_font_size):
            self.anim_button.start(self.dashboard_button)
        if self.ticket_button.font_size <= sp(self.minimum_icon_font_size):
            self.anim_button_selected.start(self.ticket_button)
        if self.settings_button.font_size >= sp(self.maximum_icon_font_size):
            self.anim_button.start(self.settings_button)
        # print(f'Button selected : {HOME_SCREEN_TICKETLIST_SCREEN}') 
        # self.parent.home_screen_manager.transition.direction = 'right'
        self.parent.home_screen_manager.current = HOME_SCREEN_TICKETLIST_SCREEN
        
        
    
    def on_settings_button_release(self, *args):
        if self.parent.home_screen_manager.current == HOME_SCREEN_TRANSACT_SCREEN:
            return
        # self.user_screen_action = 'settings'
        if self.dashboard_button.font_size >= sp(self.maximum_icon_font_size):
            self.anim_button.start(self.dashboard_button)
        if self.ticket_button.font_size >= sp(self.maximum_icon_font_size):
            self.anim_button.start(self.ticket_button)
        if self.settings_button.font_size <= sp(self.minimum_icon_font_size):
            self.anim_button_selected.start(self.settings_button) 
        # print(f'Button selected : {HOME_SCREEN_ACCOUNT_SCREEN}') 
        # self.parent.home_screen_manager.transition.direction = 'right'
        self.parent.home_screen_manager.current = HOME_SCREEN_ACCOUNT_SCREEN
    

class HomeScreen(Screen):
    
    # login_screen_manager : LoginScreenManager = None
    user_screen_action : str = StringProperty('dashboard')
    navigation_bar : NavigationBar = ObjectProperty(None)
    home_screen_manager : HomeScreenManager = ObjectProperty(None)
    content_parent : FloatLayout = ObjectProperty(None)

    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        
        self.home_screen_manager = HomeScreenManager(
            size_hint=(1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5}, 
        )
        # self.add_widget(self.home_screen_manager)

        # ✅ Create and add NavigationBar
        self.navigation_bar = NavigationBar(
            size_hint=(1, None),
            height=dp(60),
            pos_hint={"center_x": 0.5, "y": 0}
        )
        self.add_widget(self.home_screen_manager)
        self.add_widget(self.navigation_bar)
        
        self.navigation_bar.setup_butttons()  
        
        
        
        # self.home_screen_manager.transition = SlideTransition(duration=1)
        # home = Screen(name=HOME_SCREEN_DASHBOARD_SCREEN)
        # self.home_screen_manager.add_widget(home)

        # ticket_list = TicketListScreen(name=HOME_SCREEN_TICKETLIST_SCREEN)
        # self.home_screen_manager.add_widget(ticket_list)

        # account = Screen(name=HOME_SCREEN_ACCOUNT_SCREEN)
        # self.home_screen_manager.add_widget(account)
        
        # self.current = HOME_SCREEN_DASHBOARD_SCREEN

    
    # def on_kv_post(self, base_widget):
    #     if self.content_parent: 
    #         # ✅ Create and add HomeScreenManager
    #         self.home_screen_manager = HomeScreenManager(
    #             size_hint=(1, 1),
    #             pos_hint={"center_x": 0.5, "center_y": 0.5}, 
    #         )
    #         # self.add_widget(self.home_screen_manager)

    #         # ✅ Create and add NavigationBar
    #         self.navigation_bar = NavigationBar(
    #             size_hint=(1, None),
    #             height=dp(60),
    #             pos_hint={"center_x": 0.5, "y": 0}
    #         )
    #         # self.add_widget(self.navigation_bar)
    #         self.content_parent.add_widget(self.home_screen_manager)
    #         self.content_parent.add_widget(self.navigation_bar)
    #     return super().on_kv_post(base_widget)
    
    def on_pre_enter(self, *args): 
        return super().on_pre_enter(*args)
    
    
    def on_enter(self, *args):
        app = MDApp.get_running_app()  
        key = "DASHBOARD"
        # print(f'keys : {app.communications.key_running}')
        if key not in app.communications.key_running:
            app.communications.grab_dashboard()
            def communication_event(*args):
                data = app.communications.get_and_remove(key)
                if data: 
                    if data.get("result", False) == True:
                        dashboard_server_data = data.get("data", {})
                        # print(f'dashboard_server_data : {dashboard_server_data}') 
                        dashboard = self.home_screen_manager.get_screen(HOME_SCREEN_DASHBOARD_SCREEN)
                        dashboard.team_name = str(dashboard_server_data.get("team_name", "TEAM NAME"))
                        dashboard.team_member_count = str(dashboard_server_data.get("team_member_count", "0"))
                        dashboard.ticket_close_today = str(dashboard_server_data.get("ticket_close_today", "0"))
                        dashboard.open_ticket_count = str(dashboard_server_data.get("open_ticket_count", "0"))
                        dashboard.total_ticket_assigned = str(dashboard_server_data.get("ticket_assinged_total", "0"))
                        dashboard.team_member_container.clear_widgets()
                        for member in dashboard_server_data.get("members", []):
                            # print(f'member : {member}')
                            member_widget = MemberDataWidget()
                            member_widget.member_name = str(member.get("name", ""))
                            member_widget.member_ticket = str(member.get("ticket", "None"))
                            dashboard.team_member_container.add_widget(member_widget)
                        
                return False
            Clock.schedule_interval(communication_event, 1)

        return super().on_enter(*args)
            
            
            
            