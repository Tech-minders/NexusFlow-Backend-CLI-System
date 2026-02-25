import time 
from datetime import datetime, timedelta
from storage.storage import Storage
from utils.decorators import require_login
from utils.logger import Logger

#class to manage subscriptions
class Subscription:
    
    # File to store subscription data
    FILE = "data/subscriptions.json"  

    # Dictionary containing available subscription packages with name, price, and duration in hours
    PACKAGES = {
        "1": {"name": "Hourly", "price": 50, "hours": 1},
        "2": {"name": "Daily", "price": 200, "hours": 24},
        "3": {"name": "Weekly", "price": 1000, "hours": 168},
        "4": {"name": "Monthly", "price": 3000, "hours": 720},
    }
    # Stores logger instance for activity tracking
    def __init__(self, session, logger: Logger):
        self.session = session  
        self.logger = logger  
        
    # Prevent access if the user is not logged in
    @require_login(logger=None)  
    def subscribe(self):
        print("\n------ Available Packages ------")

        # Loop through all available packages and display them to the user
        for key in self.PACKAGES:
            # Get package details using its key
            package = self.PACKAGES[key]  
            print(f"{key}. {package['name']} - Kshs.{package['price']}")

        choice = input("Select package (1-4): ").strip()

        # Check if the selected package exists in the dictionary
        if choice not in self.PACKAGES:
            print("Invalid selection. Please choose a valid package.")
            return
        # Retrieve selected package details
        selected_package = self.PACKAGES[choice] 
        package_name = selected_package["name"]  
        package_price = selected_package["price"]  
        package_hours = selected_package["hours"] 

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
            f"Subscribed to {package_name}"
        )