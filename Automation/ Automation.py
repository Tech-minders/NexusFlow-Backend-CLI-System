import os
from playwright.sync_api import sync_playwright
from utils.decorators import require_login
from subscription.services import SERVICES
from subscription.subscribe import Subscription

class ServiceAutomation:

    def __init__(self, session, logger):
        
        self.session = session
        self.logger = logger
        self.subscription = Subscription(session, logger)

    @require_login  
    def access_service(self):
        
        service_key = self.session.selected_service_key
        #get service name dynamically
        service = SERVICES(service_key)
        service_name = service["name"]
        service_url = service["url"]    
        
        if not self.subscription.has_active_subscription(service_name):
            print("You do not have an active subscription for this service.")
            return
        
        user = self.session.current_user
        user_id = user["id"]
        email = user["email"]   
        
        auth_file = f"data/auth_{user_id}_{service_name}.json"
        
        print(f"Opening {service_name}...")
        
      

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            if os.path.exists(auth_file): 
                context = browser.new_context(storage_state=auth_file)
                print("Logged in automatically.")

            else:

                context = browser.new_context() 
                print("Please login manually ...") 
                
            page = context.new_page()  
            page.goto(service_url) 
             
            if not os.path.exists(auth_file):
                input("Press Enter after logging in to save session...")  
                context.storage_state(path=auth_file)
                print("session saved successfully!")

            self.logger.log(email, F"Accessed {service_name}")  
            input("Press Enter to return to CLI...") 
            
            browser.close()