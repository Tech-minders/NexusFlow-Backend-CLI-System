#CLI entry point, menu loop and routing
import os
import sys
from auth.session import Session
from auth.auth  import Signup, Login, Logout
from subscription.subscribe import Subscription
from Automation import ServiceAutomation
from utils.logger  import Logger

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

logger  = Logger()
session = Session()
signup  = Signup()
login   = Login()
logout  = Logout()

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
   # Shows who is currently logged in (or 'Not logged in').
    user = Session.current_user
    if user:
        print(f" Logged in as: {user['email']}")
    else:
        print(" Not logged in") 
    print()      


def pause():
    input("\n  Press Enter to continue...")

def divider():
    print("  " + "─" * 46)

#logout_menu
def logged_out_menu():
    divider()
    print("    [1]  Sign Up")
    print("    [2]  Log In")
    print("    [0]  Exit")
    divider()


def handle_logged_out(choice):#return True to keep it running
    if choice == "1":
        signup.signup()
        pause()
    elif choice == "2":
        login.login()
        pause()
    elif choice == "0":
        print("\n  Goodbye!\n")
        return False          
    else:
        print(" \n [!] Invalid option.please choose 1,2 or 0")
        pause()
    return True    


# Logged-in menu 

def logged_in_menu():
    divider()
    print("    [1]  Browse Services & Plans")
    print("    [2]  Subscribe to a Plan")
    print("    [3]  My Subscriptions & Access")
    print("    [4]  Cancel a Subscription")
    print("    [0]  Log Out & Exit")
    divider()


def handle_logged_in(choice):
    if choice == "1":
        sub_mgr.show_catalogue()
        pause()
    elif choice == "2":
        sub_mgr.subscribe()
        pause()
    elif choice == "3":
        sub_mgr.my_subscriptions()
        pause()
    elif choice == "4":
        sub_mgr.cancel()
        pause()
    elif choice == "0":
        logout.logout()
        pause()
    else:
        print("  [!] Invalid option.Please choose 1-4, or 0")
        pause()
    
# Main loop 
# Runs the CLI until the user exits.

def main():

    clear()
    
    while True:
        clear()
        banner()
        status_bar()
       
        if not session.current_user:
            logged_out_menu()
            print()
            choice = input(" Your choice: ").strip()
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
