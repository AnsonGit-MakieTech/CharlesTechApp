
import requests
import threading
import time

class Communications:
    server = "https://alpha.billingko.com/api/"
    token = None
    data = {}
    threads = []
    has_thread_running = False
    session = None
    is_login = False

    def __init__(self):
        self.session = requests.Session()


    def kill_all_threads(self):
        for thread in self.threads:
            thread.join()
        self.threads.clear()


    def create_session(self, username : str, password : str):
        key = "CHECK_PIN"
        def event():
            while self.has_thread_running:
                time.sleep(0.5)
            self.has_thread_running = True
            json_data = {"username": username, "password": password, "action": "technical_register_system_user"}
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
                    print(data)
                    self.data[key] = {"result" : True, "message" : "Pin exists" , "data" : data}
                else:
                    print(response.text)
                    self.data[key] = {"result" : False, "message" : "Pin does not exist"}
                
            except Exception as e:
                    self.data[key] = {"result" : False, "message" : "Error: " + str(e)}
            self.has_thread_running = False
        
        thread  = threading.Thread(target=event)
        self.threads.append(thread)
        thread.start()


    def open_by_pin(self, username : str , password : str , pin : str):
        key = "LOGIN_PIN"
        
        def event():
            while self.has_thread_running:
                time.sleep(0.5)

            self.has_thread_running = True
            json_data = {
                "username": username,
                "password": password,
                "pin": pin,
                "action": "technical_register_system_user"
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
                    self.data[key] = {"result" : False, "message" : "Registration failed"}
            except Exception as e:
                self.data[key] = {"result" : False, "message" : str(e)}

            self.has_thread_running = False
        

        thread = threading.Thread(target=event)
        self.threads.append(thread)
        thread.start()
        
        


        

    
    







