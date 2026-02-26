from Utils.decorators import require_login
from Utils.logger import Logger
from storage.storage import Storage
import os
from subscription.services import SERVICES
from datetime import datetime

class ChatGPTAutomation:

    SUBSCRIPTIONS_FILE = "data/subscriptions.json"

    def __init__(self, session, logger: Logger):
        self.session = session
        self.logger = logger 

    def _has_active_subscription(self, user_id: str, service_key: str) -> bool:
        #Return True if the user has a non-expired subscription for this service.
        subs = Storage.load(self.SUBSCRIPTIONS_FILE)
        now  = datetime.now()
        for s in subs:
            if s.get("user_id") == user_id and s.get("service_key") == service_key:
                try:
                    expiry = datetime.strptime(s["expiry"], "%Y-%m-%d %H:%M:%S")
                    if expiry > now:
                        return True
                except (ValueError, KeyError):
                    continue
        return False    

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
        
        if not self._has_active_subscription(user_id, service_key):
            print(f"\n  You don't have an active subscription for {name}.")
            print(f" Please subscribe first (option [2] from the main menu).")
            return

        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            print("\n  [!] Playwright is not installed.")
            print(" Run: pip install playwright && playwright install chromium")
            return

        print(f"Opening {name}...")
        
        auth_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            f"data/auth_{user_id}_{name}.json"  
        )

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
                
                input("\n Press Enter after logging in to save session...")  

                context.storage_state(path=auth_file)
                
                print("session saved successfully!")

            self.logger.log(email, "Accessed ChatGPT")  

            input("\n Press Enter to return to CLI...") 
            browser.close()