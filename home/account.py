from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.textinput import TextInput
from kivy.animation import Animation
from kivymd.app import MDApp
from kivy.clock import Clock
from kivy import platform
import os
import shutil

if platform == "win":
    from plyer import filechooser
if platform == "android":
    from android.storage import app_storage_path
    from androidstorage4kivy import SharedStorage, Chooser

class AccountScreen(Screen):
    no_image_path: str = StringProperty('')
    team_name: str = StringProperty('')
    fullname: str = StringProperty('')
    username: str = StringProperty('')
    email: str = StringProperty('')
    phone: str = StringProperty('')
    phone_number_editor: TextInput = ObjectProperty()
    email_editor: TextInput = ObjectProperty()
    is_loaded: bool = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        self.default_image_path = os.path.join(parent_dir, 'assets', 'profile_no_image.png')
        self.no_image_path = self.default_image_path

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
                    data = app.communications.get_and_remove(key)
                    if data and data.get("result", False):
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
    
    def update_techinfo(self, *args):
        app = MDApp.get_running_app()
        key = "UPDATE_USER_TECH_INFO"
        if key not in app.communications.key_running:
            email = self.email_editor.text
            phone = self.phone_number_editor.text 
            
            if self.no_image_path != self.default_image_path:
                image = self.no_image_path
            else:
                image = None

            self.manager.proccess_layout.open() 
            app.communications.update_user_tech_info(email = email , phone = phone , profile = image)
            def communication_event(*args):
                data = app.communications.get_and_remove(key)
                if data:
                    if data.get("result", False): 
                        self.manager.proccess_layout.display_success("User tech info updated successfully")
                        if image:
                            self.no_image_path = image
                        if email:
                            self.email_editor.text = email
                        if phone:
                            self.phone_number_editor.text = phone
                    else:
                        self.manager.proccess_layout.display_error("Failed to update user tech info")

                    return False   

            Clock.schedule_interval(communication_event, 1)  




    def upload_image(self):
        if platform == "win":
            filechooser.open_file(on_selection=self.handle_selection)
        elif platform == "android":
            self.chooser = Chooser(self.on_image_selected)
            self.chooser.choose_content('image/*', multiple=False)

    def handle_selection(self, selection):
        if selection:
            self.no_image_path = selection[0]  # Display the selected image
            print(f"Selected image path (Windows): {self.no_image_path}")

    def on_image_selected(self, uri_list):
        if uri_list:
            uri = uri_list[0] 
            ss = SharedStorage()
            private_file_path = ss.copy_from_shared(uri)
            if private_file_path:
                self.on_image_loaded_path(private_file_path)
            else:
                print("❌ Failed to copy file from shared storage.")

    def on_image_loaded_path(self, private_file_path):
        filename = os.path.basename(private_file_path)
        save_dir = os.path.join(self.get_save_path(), "selected_images")
        os.makedirs(save_dir, exist_ok=True)

        image_path = os.path.join(save_dir, filename)

        # ✅ Move or copy from temp path to your desired app location
        shutil.copy(private_file_path, image_path)

        # ✅ Set for use in Image or other display
        self.no_image_path = image_path
        print(f"✅ Saved image path: {image_path}")

    def get_save_path(self):
        # Return a writable path depending on the platform
        if platform == "android": 
            return app_storage_path()
        else:
            return os.path.expanduser("~")
