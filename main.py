#CLI entry point, menu loop and routing
import os
import sys
from auth.session import Session
from auth.auth  import Signup, Login, Logout
from subscription.subscribe import Subscription
from subscription.services  import SERVICES
from storage.storage  import Storage
from Automation.Automation import ServiceAutomation
from utils.logger  import Logger


#project root import path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

session = Session()
logger  = Logger()
signup  = Signup(session, logger)
login   = Login(session, logger)
logout  = Logout(session, logger)

sub_mgr = Subscription(session, logger)
automation = ServiceAutomation(session, logger)



# Display 
def clear():
    #Clears the terminal screen.
    os.system("cls" if os.name == "nt" else "clear")


def banner():
    #Prints the NexusFlow art banner.
    print("""
  ╔══════════════════════════════════════════════════╗
  ║    N E X U S F L O W   C L I    S Y S T E M      ║            
  ╚══════════════════════════════════════════════════╝
          """)
    
def status_bar():
   # Shows who is currently logged in or Not .
    user = session.current_user
    if user:
        print(f" Logged in as: {user['email']}")
    else:
        print(" Not logged in")   

def divider():
    print("  " + "─" * 46)

def pause():
    input("\n  Press Enter to continue...")

#logout menu
def logged_out_menu():
    divider()
    print(" [1]  Sign Up")
    print(" [2]  Log In")
    print(" [0]  Exit")
    divider()


def handle_logged_out(choice):#return True to keep it running
    if choice == "1":
        signup.signup()
        pause()
    elif choice == "2":
        login.login()
        pause()
    elif choice == "0":
        print(" \n Goodbye!\n")
        return False          
    else:
        print("  [!] Invalid option.please choose 1,2 or 0")
        pause()
    return True               


# Logged-in menu 

def logged_in_menu():
    divider()
    print("    [1]  Browse Services & Plans")
    print("    [2]  Subscribe to a Plan")
    print("    [3]  My Subscriptions")
    print("    [4]  Access a Service")
    print("    [5]  Cancel a Subscription")
    print("    [0]  Log Out & Exit")
    divider()

def show_catalogue():

    print("\n  === Available Services ===")
    for key, service in SERVICES.items():
        print(f"\n  [{key}] {service['name']}")
        for pkg_key, pkg in service["packages"].items():
            print(f"  {pkg_key}. {pkg['name']:10s}  Kshs.{pkg['price']}")

def handle_logged_in(choice: str):
    if choice == "1":
        show_catalogue()
        pause()

    elif choice == "2":
        show_catalogue()
        service_key = input("\n  Enter service number to subscribe to: ").strip()
        if service_key not in SERVICES:
            print("  [!] Invalid service number.")
            pause()
            return
        session.selected_service_key = service_key
        sub_mgr.subscribe()

    elif choice == "3":
        sub_mgr.list_active()
        pause()

    elif choice == "4":
        sub_mgr.list_active()
        service_key = input("\n  Enter service number to access: ").strip()
        if service_key not in SERVICES:
            print("  [!] Invalid service number.")
            pause()
            return
        automation.access_service(service_key)
        pause()

    elif choice == "5":
         sub_mgr.list_active()
         sub_mgr.cancel()
         pause()     

    elif choice == "0":
        logout.logout()
        pause()
    else:
        print("  [!] Invalid option.Please choose 1-5, or 0")
        pause()
    return True 


# Main loop 
# Runs the CLI until the user exits.

def main():
    clear()
    
    while True:
        clear()
        banner()
        if session.is_expired():
            print("\n  [!] Session expired due to inactivity. Please log in again.")
            session.expire()
        status_bar()
        print()
        
        if not session.current_user:
            logged_out_menu()
            print()
            choice = input("  Your choice: ").strip()
            print()
            keep_running = handle_logged_out(choice)
            if not keep_running:
                break
        else:
            logged_in_menu()
            print()
            choice = input("  Your choice: ").strip()
            print()
            handle_logged_in(choice)



#Entry point 

if __name__ == "__main__":

    main()
