#CLI entry point, menu loop and routing
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from auth.session import session
from auth.auth  import Signup, Login, Logout
from subscription.subscribe import SubscriptionManager
from utils.logger  import Logger

logger  = Logger()
signup  = Signup()
login   = Login()
logout  = Logout()
sub_mgr = SubscriptionManager()


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
   # Shows who is currently logged in (or 'Not logged in').
    user = session.get("user")
    if user:
        print(f" Logged in as: {user['email']}")
    else:
        print(" Not logged in")   


def pause():
    input("\n  Press Enter to continue...")


def logged_out_menu():
    print("  " + "─" * 46)
    print("    [1]  Sign Up")
    print("    [2]  Log In")
    print("    [0]  Exit")
    print("  " + "─" * 46)


def handle_logged_out(choice: str):
    if choice == "1":
        signup.signup()
        pause()
    elif choice == "2":
        login.login()
        pause()
    elif choice == "0":
        print("  Goodbye!\n")
        return False          # signals main loop to exit
    else:
        print("  [!] Invalid option.")
        pause()
    return True               # keep running


# Logged-in menu 

def logged_in_menu():
    print("  " + "─" * 46)
    print("    [1]  Browse Services & Plans")
    print("    [2]  Subscribe to a Plan")
    print("    [3]  My Subscriptions & Access")
    print("    [4]  Cancel a Subscription")
    print("    [0]  Log Out & Exit")
    print("  " + "─" * 46)


def handle_logged_in(choice: str):
    if choice == "1":
        SubscriptionManager.show_catalogue()
        pause()
    elif choice == "2":
        sub_mgr.subscribe()
        pause()
    elif choice == "3":
        # my_subscriptions() shows the table AND handles Access in one flow
        sub_mgr.my_subscriptions()
        pause()
    elif choice == "4":
        sub_mgr.cancel()
        pause()
    elif choice == "0":
        logout.logout()
        pause()
    else:
        print("  [!] Invalid option.")
        pause()
    return True               # always keep running 
# Main loop 
# Runs the CLI until the user exits.

def main():
    clear()
    
    while True:
        clear()
        banner()
        status_bar()
        
        user = session.get("user")
        if not user:
            logged_out_menu()
            print()
            choice = input("  Your choice: ").strip()
            print()
            running = handle_logged_out(choice)
        else:
            logged_in_menu()
            print()
            choice = input("  Your choice: ").strip()
            print()
            handle_logged_in(choice)



#Entry point 

if __name__ == "__main__":

    main()
