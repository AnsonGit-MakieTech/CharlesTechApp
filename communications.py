
import requests
import threading
import time
import os
import base64

from utils.app_utils import has_internet
import variables

class Communications:
    # server = "https://charlescatv.billingko.com/api/" # OFFICIAL SERVER
    server = "https://alpha.billingko.com/api/" # DUMMY SERVER
    token = None
    data = {}
    threads = []
    has_thread_running = False
    session = None
    is_login = False
    
    key_running = []

    def __init__(self):
        self.session = requests.Session()


    def kill_all_threads(self):
        for thread in self.threads:
            thread.join()
        self.threads.clear()

    def get_and_remove(self, key : str):
        if key in self.data:
            value = self.data[key]
            del self.data[key]
            return value
        return dict()
    
    def is_running(self):
        if len(self.threads) > 0:
            return True
        return False

    def create_session(self, username : str, password : str):
        key = "CHECK_PIN"
        def event(self_thread):
            while self.has_thread_running:
                time.sleep(0.5)
            self.has_thread_running = True
            self.key_running.append(key)

            if not has_internet():
                self.data[key] = {"result" : "NA", "message" : "No Internet Connection"}
                self.has_thread_running = False
                self.key_running.remove(key) 
                if self_thread in self.threads:
                    self.threads.remove(self_thread) 
                return

            json_data = {
                "username": username, 
                "password": password, 
                "action": "technical_register_system_user",
                "version" : variables.VERSION_APP
            }
            # csrf_token = self.session.cookies.get('csrftoken')  # Django sets this
            url = self.server + "technical_unauthenticated_api"
            headers = {
                "Content-Type": "application/json",
                # "X-CSRFToken": csrf_token,
                # "Referer": url,  # important if Django checks referer
                # "Origin": self.server,
                "User-Agent": "KivyApp/1.0.0",
            } 
            try:
                response = self.session.post(url, headers=headers, json=json_data)
                if response.ok:
                    data = response.json() 
                    self.data[key] = {"result" : True, "message" : "Verified Users!" , "data" : data}
                else:
                    # print(response.text)
                    data = response.json()
                    message = data.get("text", "No Pin Found! Please Register!")
                    self.data[key] = {"result" : False, "message" : message}
                
            except Exception as e:
                    self.data[key] = {"result" : False, "message" : "Error: " + str(e)}
            self.has_thread_running = False
            self.key_running.remove(key)

            if self_thread in self.threads:
                self.threads.remove(self_thread)
            
        
        thread = threading.Thread(target=lambda: event(thread))
        self.threads.append(thread)
        thread.start()


    def open_by_pin(self, username : str , password : str , pin : str):
        key = "LOGIN_PIN"
        
        def event(self_thread):
            while self.has_thread_running:
                time.sleep(0.5)
            
            if not has_internet():
                self.data[key] = {"result" : "NA", "message" : "No Internet Connection"}
                self.has_thread_running = False
                self.key_running.remove(key) 
                if self_thread in self.threads:
                    self.threads.remove(self_thread) 
                return

            self.has_thread_running = True
            self.key_running.append(key)
            json_data = {
                "username": username,
                "password": password,
                "pin": pin,
                "action": "verify_pin",
                "version" : variables.VERSION_APP
            }            
            url = self.server + "technical_unauthenticated_api"
            headers = {
                "Content-Type": "application/json",
                # "X-CSRFToken": csrf_token,
                # "Referer": url,  # important if Django checks referer
                # "Origin": self.server,
                "User-Agent": "KivyApp/1.0.0",
            }
            try:
                response = self.session.post(url, headers=headers, json=json_data , timeout=(3, 5)) 
                if response.ok:
                    data = response.json()
                    # print(data)
                    self.data[key] = {"result" : True, "message" : "Logging In!" , "data" : data}
                else:
                    data = response.json()
                    message = data.get("text", "Incorrect Pin!")
                    self.data[key] = {"result" : False, "message" : message}
            except Exception as e:
                self.data[key] = {"result" : False, "message" : "Server Is Down" } 

            self.has_thread_running = False
            self.key_running.remove(key)
            if self_thread in self.threads:
                self.threads.remove(self_thread)
        
 
        thread = threading.Thread(target=lambda: event(thread))
        self.threads.append(thread)
        thread.start()
        
    
    def register_pin(self, username : str , password : str , pin : str):
        key = "REGISTER_PIN"  
        
        def event(self_thread):
            while self.has_thread_running:
                time.sleep(0.5)

            if not has_internet():
                self.data[key] = {"result" : "NA", "message" : "No Internet Connection"}
                self.has_thread_running = False
                self.key_running.remove(key) 
                if self_thread in self.threads:
                    self.threads.remove(self_thread) 
                return

            self.has_thread_running = True
            self.key_running.append(key)
            json_data = {
                "username": username,
                "password": password,
                "new_pin": pin,
                "action": "register_new_pin",
                "version" : variables.VERSION_APP
            }            
            url = self.server + "technical_unauthenticated_api"
            headers = {
                "Content-Type": "application/json",
                # "X-CSRFToken": csrf_token,
                # "Referer": url,  # important if Django checks referer
                # "Origin": self.server,
                "User-Agent": "KivyApp/1.0.0",
            }
            try:
                response = self.session.post(url, headers=headers, json=json_data)
                if response.ok:
                    data = response.json()

                    self.data[key] = {"result" : True, "message" : "Registration successful" , "data" : data}
                else:
                    data = response.json()
                    message = data.get("text", "Registration failed")
                    self.data[key] = {"result" : False, "message" : message}
            except Exception as e:
                self.data[key] = {"result" : False, "message" : str(e)}

            self.has_thread_running = False
            self.key_running.remove(key)
            if self_thread in self.threads:
                self.threads.remove(self_thread)
        

        
        thread = threading.Thread(target=lambda: event(thread))
        self.threads.append(thread)
        thread.start()


    def grab_dashboard(self):
        key = "DASHBOARD"
        
        
        
        def event(self_thread):
            while self.has_thread_running:
                time.sleep(0.5)

            if not has_internet():
                self.data[key] = {"result" : "NA", "message" : "No Internet Connection"}
                self.has_thread_running = False
                self.key_running.remove(key) 
                if self_thread in self.threads:
                    self.threads.remove(self_thread)
                return

            self.has_thread_running = True
            self.key_running.append(key)
            json_data = { 
                "action": "grab_dashboard"
            }            
            url = self.server + "technical_center_api"
            headers = {
                "Content-Type": "application/json",
                # "X-CSRFToken": csrf_token,
                # "Referer": url,  # important if Django checks referer
                # "Origin": self.server,
                "User-Agent": "KivyApp/1.0.0",
            }
            try:
                response = self.session.post(url, headers=headers, json=json_data)
                if response.ok:
                    data = response.json() 
                    # print(data)
                    self.data[key] = {"result" : True, "message" : "" , "data" : data}
                else:
                    # print(response.text)
                    self.data[key] = {"result" : False, "message" : ""}
            except Exception as e:
                self.data[key] = {"result" : False, "message" : str(e)}

            self.has_thread_running = False
            self.key_running.remove(key)
            if self_thread in self.threads:
                self.threads.remove(self_thread)
        

        
        thread = threading.Thread(target=lambda: event(thread))
        self.threads.append(thread)
        thread.start()


    def get_ticket_list(self):
        key = "TICKET_LIST"
        
        

        def event(self_thread):
            while self.has_thread_running:
                time.sleep(0.5)
            self.has_thread_running = True
            self.key_running.append(key)

            json_data = {
                "action": "grab_all_open_tickets"
            }
            url = self.server + "technical_center_api"
            headers = {
                "Content-Type": "application/json",
                # "X-CSRFToken": csrf_token,
                # "Referer": url,  # important if Django checks referer
                # "Origin": self.server,
                "User-Agent": "KivyApp/1.0.0",
            }
            try:
                response = self.session.post(url, headers=headers, json=json_data)
                if response.ok:
                    data = response.json()
                    self.data[key] = {"result" : True, "message" : "" , "data" : data.get('tickets',[])}
                    # print("Tikect data : ", data)
                else:
                    # print("Tikect data : ", None)
                    self.data[key] = {"result" : False, "message" : ""}
            except Exception as e:
                self.data[key] = {"result" : False, "message" : str(e)}
                # print("Tikect data error: ", None)
            self.has_thread_running = False
            self.key_running.remove(key)
            if self_thread in self.threads:
                self.threads.remove(self_thread)
            
        
        thread = threading.Thread(target=lambda: event(thread))
        self.threads.append(thread)
        thread.start()
 
    def get_user_tech_info(self):
        key = "GET_USER_TECH_INFO"
        
        def event(self_thread):
            while self.has_thread_running:
                time.sleep(0.5)
            self.has_thread_running = True
            self.key_running.append(key)

            json_data = {
                "action": "grab_technical_settings"
            }
            url = self.server + "technical_center_api"
            headers = {
                "Content-Type": "application/json",
                # "X-CSRFToken": csrf_token,
                # "Referer": url,  # important if Django checks referer
                # "Origin": self.server,
                "User-Agent": "KivyApp/1.0.0",
            }
            try:
                response = self.session.post(url, headers=headers, json=json_data)
                if response.ok:
                    data = response.json()
                    self.data[key] = {"result" : True, "message" : "" , "data" : data}
                else:
                    # print(response.text)
                    self.data[key] = {"result" : False, "message" : ""}
            except Exception as e:
                self.data[key] = {"result" : False, "message" : str(e)}
            self.has_thread_running = False
            self.key_running.remove(key)
            if self_thread in self.threads:
                self.threads.remove(self_thread)

        
        thread = threading.Thread(target=lambda: event(thread))
        self.threads.append(thread)
        thread.start()


    def update_user_tech_info(self, email = None , phone = None , profile = None):
        key = "UPDATE_USER_TECH_INFO"
        def event(self_thread):
            while self.has_thread_running:
                time.sleep(0.5)
            self.has_thread_running = True
            self.key_running.append(key)

            json_data = {
                "action": "update_technical_settings"
            }
            if email:
                json_data["email"] = email
            if phone:
                json_data["phone"] = phone

            if profile: 
                if profile or os.path.exists(profile):
                    with open(profile, "rb") as f:
                        encoded_image = base64.b64encode(f.read()).decode("utf-8")

                    # You can also extract the file extension if needed
                    file_ext = os.path.splitext(profile)[1].replace('.', '')  # jpg, png, etc.

                    json_data["profilepic"] = encoded_image
                    json_data["profilepic_ext"] = file_ext  

            url = self.server + "technical_center_api"
            headers = {
                "Content-Type": "application/json",
                # "X-CSRFToken": csrf_token,
                # "Referer": url,  # important if Django checks referer
                # "Origin": self.server,
                "User-Agent": "KivyApp/1.0.0",
            }
            try:
                response = self.session.post(url, headers=headers, json=json_data)
                if response.ok:
                    data = response.json()
                    self.data[key] = {"result" : True, "message" : "" , "data" : data}
                else:
                    # print(response.text)
                    self.data[key] = {"result" : False, "message" : ""}
            except Exception as e:
                self.data[key] = {"result" : False, "message" : str(e)}
            self.has_thread_running = False
            self.key_running.remove(key)
            if self_thread in self.threads:
                self.threads.remove(self_thread)

        
        thread = threading.Thread(target=lambda: event(thread))
        self.threads.append(thread)
        thread.start()


    def ticket_next_step(self, data = dict):
        key = "TICKET_NEXT_STEP"
        def event(self_thread , data):
            while self.has_thread_running:
                time.sleep(0.5)
            self.has_thread_running = True
            self.key_running.append(key)

            json_data = {
                "action": "ticket_next_step"
            }
            for dkey in data:
                json_data[dkey] = data[dkey]
            url = self.server + "technical_center_api"
            headers = {
                "Content-Type": "application/json",
                # "X-CSRFToken": csrf_token,
                # "Referer": url,  # important if Django checks referer
                # "Origin": self.server,
                "User-Agent": "KivyApp/1.0.0",
            }
            # print("payload : ", json_data)
            try:
                response = self.session.post(url, headers=headers, json=json_data)
                # # print(response.text)
                
                if response.ok:
                    data = response.json()
                    # # print(data)
                    self.data[key] = {"result" : True, "message" : data.get("text", "Successfully processed"), "data" : data}
                else: 
                    data = response.json()
                    self.data[key] = {"result" : False, "message" : data.get("text" ,"There is a problem in the server")}
                # # print(data)
            except Exception as e:
                self.data[key] = {"result" : False, "message" : "Please Check Your Internet Connection"}
            self.has_thread_running = False
            self.key_running.remove(key)
            if self_thread in self.threads:
                self.threads.remove(self_thread)

        
        thread = threading.Thread(target=lambda: event(thread, data))
        self.threads.append(thread)
        thread.start()


    def forgot_pin(self, username : str, password : str, new_pin : str):
        key = "FORGOT_PIN"
        def event(self_thread):
            while self.has_thread_running:
                time.sleep(0.5)
            self.has_thread_running = True
            self.key_running.append(key)

            if not has_internet():
                self.data[key] = {"result" : "NA", "message" : "No Internet Connection"}
                self.has_thread_running = False
                self.key_running.remove(key) 
                if self_thread in self.threads:
                    self.threads.remove(self_thread) 
                return

            json_data = {
                "username": username, 
                "password": password, 
                "new_pin": new_pin, 
                "action": "reset_pin",
                "version" : variables.VERSION_APP
                }
            # csrf_token = self.session.cookies.get('csrftoken')  # Django sets this
            url = self.server + "technical_unauthenticated_api"
            headers = {
                "Content-Type": "application/json",
                # "X-CSRFToken": csrf_token,
                # "Referer": url,  # important if Django checks referer
                # "Origin": self.server,
                "User-Agent": "KivyApp/1.0.0",
            } 
            try:
                response = self.session.post(url, headers=headers, json=json_data)
                if response.ok:
                    data = response.json() 
                    self.data[key] = {"result" : True, "message" : "Verified Users!" , "data" : data}
                else:
                    # print(response.text)
                    data = response.json()
                    message = data.get("text",  "No Pin Found! Please Register!")
                    self.data[key] = {"result" : False, "message" : message}
                
            except Exception as e:
                    self.data[key] = {"result" : False, "message" : "Error: " + str(e)}
            self.has_thread_running = False
            self.key_running.remove(key)

            if self_thread in self.threads:
                self.threads.remove(self_thread)
            
        
        thread = threading.Thread(target=lambda: event(thread))
        self.threads.append(thread)
        thread.start()


    def reset_pin(self, old_pin : str, new_pin : str, confirm_pin : str):
        key = "RESET_PIN"
        def event(self_thread):
            while self.has_thread_running:
                time.sleep(0.5)
            self.has_thread_running = True
            self.key_running.append(key)

            json_data = {
                "action": "update_pin",
                "old_pin": old_pin,
                "new_pin": new_pin,
                "confirm_pin": confirm_pin,
                "version" : variables.VERSION_APP
            } 
            url = self.server + "technical_center_api"
            headers = {
                "Content-Type": "application/json",
                # "X-CSRFToken": csrf_token,
                # "Referer": url,  # important if Django checks referer
                # "Origin": self.server,
                "User-Agent": "KivyApp/1.0.0",
            }
            try:
                response = self.session.post(url, headers=headers, json=json_data)
                if response.ok:
                    data = response.json()
                    self.data[key] = {"result" : True, "message" : "" , "data" : data}
                else:
                    # print(response.text)
                    self.data[key] = {"result" : False, "message" : ""}
            except Exception as e:
                self.data[key] = {"result" : False, "message" : str(e)}
            self.has_thread_running = False
            self.key_running.remove(key)
            if self_thread in self.threads:
                self.threads.remove(self_thread)

        
        thread = threading.Thread(target=lambda: event(thread))
        self.threads.append(thread)
        thread.start()

    def add_remarks(self, ticket_id : str, title : str, remarks : str):
        key = "ADD_REMARKS"
        def event(self_thread):
            while self.has_thread_running:
                time.sleep(0.5)
            self.has_thread_running = True
            self.key_running.append(key)

            json_data = {
                "action": "add_ticket_remarks",
                "title": title,
                "ticket_id": ticket_id,
                "remarks": remarks
            } 
            url = self.server + "technical_center_api"
            headers = {
                "Content-Type": "application/json",
                # "X-CSRFToken": csrf_token,
                # "Referer": url,  # important if Django checks referer
                # "Origin": self.server,
                "User-Agent": "KivyApp/1.0.0",
            }
            try:
                response = self.session.post(url, headers=headers, json=json_data)
                if response.ok:
                    data = response.json()
                    self.data[key] = {"result" : True, "message" : "Successfully added remarks" , "data" : data}
                else:
                    # print(response.text)
                    self.data[key] = {"result" : False, "message" : "Failed to add remarks"}
            except Exception as e:
                self.data[key] = {"result" : False, "message" : str(e)}
            self.has_thread_running = False
            self.key_running.remove(key)
            if self_thread in self.threads:
                self.threads.remove(self_thread)

        
        thread = threading.Thread(target=lambda: event(thread))
        self.threads.append(thread)
        thread.start()

    def refetch_remarks(self, ticket_id : str):
        key = "REFETCH_REMARKS"
        def event(self_thread):
            while self.has_thread_running:
                time.sleep(0.5)
            self.has_thread_running = True
            self.key_running.append(key)

            json_data = {
                "action": "get_remarks_by_ticket",
                "ticket_id": ticket_id, 
            } 
            url = self.server + "technical_center_api"
            headers = {
                "Content-Type": "application/json",
                # "X-CSRFToken": csrf_token,
                # "Referer": url,  # important if Django checks referer
                # "Origin": self.server,
                "User-Agent": "KivyApp/1.0.0",
            }
            try:
                response = self.session.post(url, headers=headers, json=json_data)
                if response.ok:
                    data = response.json()
                    self.data[key] = {"result" : True, "message" : "Successfully added remarks" , "data" : data}
                else:
                    # print(response.text)
                    self.data[key] = {"result" : False, "message" : "Failed to add remarks"}
            except Exception as e:
                self.data[key] = {"result" : False, "message" : str(e)}
            self.has_thread_running = False
            self.key_running.remove(key)
            if self_thread in self.threads:
                self.threads.remove(self_thread)

        
        thread = threading.Thread(target=lambda: event(thread))
        self.threads.append(thread)
        thread.start()




