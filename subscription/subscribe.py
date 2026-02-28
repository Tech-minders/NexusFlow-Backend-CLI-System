import time
import uuid
from datetime import datetime, timedelta
from storage.storage import Storage
from Utils.decorators import require_login
from Utils.logger import Logger
from subscription.services import SERVICES

#class to manage subscriptions
class Subscription:
    
    # File path to store subscription data
    FILE = "data/subscriptions.json"  

    # Stores logger instance for activity tracking
    def __init__(self, session, logger: Logger):
        self.session = session  
        self.logger = logger  
        
 # Return current logged-in user object
    @property
    def current_user(self):
        return self.session.current_user

    # Return logged-in user's email
    @property
    def user_email(self):
        return self.current_user["email"]

    # Return logged-in user's ID
    @property
    def user_id(self):
        return self.current_user["id"]

    # Load subscriptions from storage file
    def _load_subscriptions(self):
        return Storage.load(self.FILE)

    # Save subscriptions to storage file
    def _save_subscriptions(self, subscriptions):
        Storage.save(self.FILE, subscriptions)

    # Create a new subscription object
    def _create_subscription(
        self,
        service_name,
        package_name,
        package_price,
        start_date,
        expiry_date
    ):
        
        return {
            "id": str(uuid.uuid4())[:8],  
            "user_id": self.user_id,
            "email": self.user_email, 
            "service": service_name,  
            "package": package_name, 
            "price": package_price, 
            "start_date": start_date.strftime("%Y-%m-%d %H:%M:%S"),
            "expiry": expiry_date.strftime("%Y-%m-%d %H:%M:%S"), 
            "status": "active"
        }

    # Allow user to subscribe to a service package
    @require_login
    def subscribe(self):

        service_key = self.session.selected_service_key
        # Validate selected service
        if not service_key or service_key not in SERVICES:
            print("No service selected")
            return
        # Extract service details
        service = SERVICES[service_key]  
        service_name = service["name"]
        packages = service["packages"]

        print(f"\n=== {service_name} Packages ===")

        # Display available packages
        for key, package in packages.items():
            print(f"\n{key}. {package['name']} - Kshs.{package['price']}")

        choice = input("Select package: ").strip()  # Get user selection

        # Validate package selection
        if choice not in packages:
            print("Invalid selection.")
            return
        
        # Extract selected package details
        package = packages[choice]  
        package_name = package["name"]
        package_price = package["price"]
        package_hours = package["hours"]

        print(f"\nYou selected {package_name} package")
        print(f"Amount to pay: Kshs.{package_price}")

        # Ask user to confirm payment
        confirm = input("Proceed with payment? (y/n): ").lower()

        if confirm != "y":
            print("Payment cancelled.")
            return

        print(f"Processing payment of Kshs.{package_price}...")
        # Simulate payment processing delay
        time.sleep(1)  
        
        # Record subscription start time and calculate expiry date
        start_date = datetime.now()  
        expiry_date = start_date + timedelta(hours=package_hours) 
        
        # Load existing subscriptions
        subscriptions = self._load_subscriptions() 
        
        # Create new subscription object
        new_subscription = self._create_subscription(
            service_name,
            package_name,
            package_price,
            start_date,
            expiry_date
        )

        subscriptions.append(new_subscription)
        
        # Save updated subscriptions
        self._save_subscriptions(subscriptions)  

        print("\nSubscription successful!")
        print("--------------------------")
        print(f"Service: {service_name}")
        print(f"Package: {package_name}")
        print(f"Expires on: {expiry_date.strftime('%Y-%m-%d %H:%M:%S')}")
        print("--------------------------")

        # Log subscription activity
        self.logger.log(
            self.user_email,
            f"Subscribed to {service_name} ({package_name})"
        )

    # List active subscriptions for current user
    @require_login
    def list_active(self):

        subscriptions = self._load_subscriptions()

        # Filter active subscriptions for current user
        active = [
            sub for sub in subscriptions
            if sub["email"] == self.user_email
            and sub["status"] == "active"
        ]

        if not active:
            print("No active subscriptions.")
            return

        print("\nYour active subscriptions:")

        # Display active subscriptions
        for sub in active:
            print("--------------------------")
            print(f"ID: {sub['id']}")
            print(f"Service: {sub['service']}")
            print(f"Package: {sub['package']}")
            print(f"Expiry: {sub['expiry']}")
            print(f"Status: {sub['status']}")
            print("--------------------------")

    # Check if user has active subscription for a service
    def has_active_subscription(self, service_name):

        subscriptions = self._load_subscriptions()
        now = datetime.now() 
        for sub in subscriptions:
            #Skip other users, other services, and inactive subscriptions.
            if sub["email"] != self.user_email:
                continue 
            if sub["service"] != service_name:
                continue 
            if sub["status"] != "active":
                continue

            expiry = datetime.strptime(
                sub["expiry"],
                "%Y-%m-%d %H:%M:%S"
            )
            # Active subscription exists
            if expiry > now:
                return True  
        # No active subscription
        return False 

    # Cancel an existing subscription
    @require_login
    def cancel(self):

        subscriptions = self._load_subscriptions()
        subscription_id = input("Enter subscription ID to cancel: ")

        for sub in subscriptions:

            # Match subscription ID and current user
            if sub["id"] == subscription_id and sub["email"] == self.user_email:
                sub["status"] = "cancelled"
                self._save_subscriptions(subscriptions)
                print("Subscription cancelled.")
                # Log cancellation
                self.logger.log(
                    self.user_email,
                    f"Cancelled subscription {subscription_id}"
                )
                return

        print("Subscription not found.")