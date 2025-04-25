

from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
import os
from kivy.animation import Animation
from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy import platform
from kivy.uix.textinput import TextInput

if platform in ["android", "win"]:
    from plyer import filechooser


class AccountScreen(Screen):

    no_image_path : str = StringProperty('')
    team_name : str = StringProperty('')
    fullname : str  = StringProperty('')
    username : str = StringProperty('')
    email : str = StringProperty('')
    phone : str = StringProperty('')
    phone_number_editor : TextInput = ObjectProperty()
    email_editor : TextInput = ObjectProperty()
    is_loaded : bool = False
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        self.no_image_path = os.path.join(parent_dir, 'assets', 'profile_no_image.png')

    
    def on_leave(self, *args):
        Animation(opacity=0, duration=0.5).start(self)
        return super().on_leave(*args)
    
    def on_enter(self, *args):  
        if not self.is_loaded:
            app = MDApp.get_running_app()  
            key = "GET_USER_TECH_INFO" 
            if key not in app.communications.key_running:
                app.communications.get_user_tech_info()
                def communication_event(*args):
                    
                    data = app.communications.data.get(key, None)
                    if data: 
                        if data.get("result", False) == True:
                            self.is_loaded = True
                            tect_server_data = data.get("data", {}) 
                            self.team_name = tect_server_data.get("team_name", "")
                            self.fullname = f'{tect_server_data.get("fname", "")} {tect_server_data.get("lname", "")}'
                            self.username = tect_server_data.get("username", "") 
                            self.email_editor.text = tect_server_data.get("email", "")
                            self.phone_number_editor.text = tect_server_data.get("phone", "")
                            self.email = f'[font=roboto_semibold]Email :[/font]    [font=roboto_light]{tect_server_data.get("email", "")}[/font]'
                            self.phone = f'[font=roboto_semibold]Phone Number : [/font]    [font=roboto_light]{tect_server_data.get("phone", "")}[/font]'
                            url_image = tect_server_data.get("profilepic", None)
                            if url_image:
                                self.no_image_path = url_image
                            
                    return False
                
                Clock.schedule_interval(communication_event, 1)

        Animation(opacity=1, duration=0.5).start(self)  
        return super().on_enter(*args)



    def upload_image(self):
        if platform in ["android", "win"]:
            filechooser.open_file(on_selection=self.handle_selection)

    def handle_selection(self, selection):
        if selection:
            self.selected_image = selection[0]
            print(f"Selected image path: {self.selected_image}")

    
