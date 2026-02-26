from utils.decorators import require_login
from utils.logger import Logger
from playwright.sync_api import sync_playwright
import os
from subscription.services import SERVICES

class ChatGPTAutomation:

    def __init__(self, session, logger: Logger):
        self.session = session
        self.logger = logger 

    @require_login(logger=None)  
    def access_service(self):
        
        service_key = self.session.selected_service_key
        
        if not service_key or service_key not in SERVICES:
            
            print("No service selected.")
            return
        
        service = SERVICES[service_key]
        
        url = service["url"]
        
        name = service["name"]
        
        user = self.session.current_user
        
        user_id = user["id"]
        
        email = user["email"]   
        

        print(f"Opening {name}...")
        
        auth_file = f"data/auth_{user_id}_{name}.json"  

        with sync_playwright() as p:
            
            browser = p.chromium.launch(headless=False)
            
            if os.path.exists(auth_file): 

                context = browser.new_context(storage_state=auth_file)
                
                page = context.new_page() 
                 
                page.goto(url)  

                print("Logged in automatically using saved session.")

            else:

                context = browser.new_context() 
                 
                page = context.new_page()  
                
                page.goto(url)  

                print("Please log in manually ...")
                
                input("Press Enter after logging in to save session...")  

                context.storage_state(path=auth_file)
                
                print("session saved successfully!")

            self.logger.log(email, "Accessed ChatGPT")  

            input("Press Enter to return to CLI...") 
            browser.close()