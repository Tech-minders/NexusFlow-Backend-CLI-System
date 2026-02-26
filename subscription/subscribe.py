import time 
from datetime import datetime, timedelta
from storage.storage import Storage
from utils.decorators import require_login
from utils.logger import Logger
from subscription.services import SERVICES

#class to manage subscriptions
class Subscription:
    
    # File to store subscription data
    FILE = "data/subscriptions.json"  

    # Stores logger instance for activity tracking
    def __init__(self, session, logger: Logger):
        self.session = session  
        self.logger = logger  
        
    # Prevent access if the user is not logged in
    @require_login(logger=None)  
    def subscribe(self):
        
        #retrieve service selected by user from the session object
        service_key = self.session.selected_service_key
        # validate the selected service
        if not service_key or service_key not in SERVICES:
            print("No service selected")
            return
        #retrieve service from service dictionary
        service = SERVICES[service_key]
        service_name = service["name"]
        packages = service["packages"]
        
        print("\n------ {service_name} Packages ------")

        # Loop through all available packages and display them to the user
        
        for key, package in packages.items(): 
            print(f"{key}. {package['name']} - Kshs.{package['price']}")

        choice = input("Select package: ").strip()

        # Check if the selected package exists in the service dictionary
        if choice not in packages:
            print("Invalid selection. Please choose a valid package.")
            return
        # Retrieve selected package details
        package = packages[choice]
        package_name = package['name']
        package_price = package['price']
        package_hours = package['hours']

        print(f"\nYou selected {package_name}")
        print(f"Amount to pay: Kshs.{package_price}")

        # convert user payment input into a float number
        try:
            amount_paid = float(input("Enter amount to pay: Kshs.").strip())
        except ValueError:
            print("Invalid amount entered.")
            return

        # Check if the payment is less than the required amount
        if amount_paid < package_price:
            print("Insufficient payment. Subscription cancelled.")
            return

        # Handle case where user pays more than required
        elif amount_paid > package_price:
            print("Payment exceeds required amount. Processing exact package price...")

        print("Processing payment...")
        time.sleep(1)
        
        # Calculate expiry date using hours
        expiry = datetime.now() + timedelta(hours=package_hours)
        
        # Load existing subscriptions from file
        subscriptions = Storage.load(self.FILE)

        # Append new subscription details to the subscriptions list
        subscriptions.append({
            "user_id": self.session.current_user["id"], 
            "service_key": service_key,
            "service": service_name,
            "package": package_name, 
            "price": package_price, 
            "expiry": expiry.strftime("%Y-%m-%d %H:%M:%S") 
        })
        # Save updated subscriptions back to file
        Storage.save(self.FILE, subscriptions)  

        print(f"\nSubscription successful!") 
        print(f"Package: {package_name}") 
        print(f"Expires on: {expiry.strftime('%Y-%m-%d %H:%M:%S')}")

        # Log subscription action using the logger class
        self.logger.log(
            self.session.current_user["email"],
            f"Subscribed to {service_name} ({package_name})"
        )