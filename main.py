#CLI entry point, menu loop and routing
import os
import sys
from datetime import datetime

#project root import path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from auth.session import Session
from auth.auth  import Signup, Login, Logout
from subscription.subscribe import Subscription
from subscription.services  import SERVICES
from storage.storage  import Storage
from Utils.logger  import Logger

session = Session()
logger  = Logger()
signup  = Signup(session, logger)
login   = Login(session, logger)
logout  = Logout(session, logger)
sub = Subscription(session, logger)


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


def handle_logged_out(choice: str):
    if choice == "1":
        signup.signup()
        pause()
    elif choice == "2":
        login.login()
        if not session.current_user:
            pause()
    elif choice == "0":
        print(" \n Goodbye!\n")
        return False          # signals main loop to exit
    else:
        print("  [!] Invalid option.")
        pause()
    return True               # keep running


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


def handle_logged_in(choice: str):
    if choice == "1":
        show_catalogue()
        pause()
    elif choice == "2":
        select_service_then("subscribe")
    elif choice == "3":
        my_subscriptions()
        pause()
    elif choice == "4":
        select_service_then("access")
    elif choice == "5":
        cancel_subscription()
        pause()
    elif choice == "0":
        logout.logout()
        pause()
    else:
        print("  [!] Invalid option.")
        pause()
    return True 


 #FEATURE SCREENS


def show_catalogue():
    #Display every service and its packages in a formatted table.
    clear()
    banner()
    print("  AVAILABLE SERVICES & PLANS\n")
    for svc_key, svc in SERVICES.items():
        print(f"  ┌─ [{svc_key}]  {svc['name']}")
        print(f"  │   {svc['url']}")
        for pkg_key, pkg in svc["packages"].items():
            print(f"  │   [{pkg_key}]  {pkg['name']:<10}  Kshs. {pkg['price']:>5}  ({pkg['hours']}h)")
        print("  │")


def select_service_then(action):
  
    clear()
    banner()
    print("  SELECT A SERVICE\n")
    for key, svc in SERVICES.items():
        print(f"    [{key}]  {svc['name']}")
    divider()
    choice = input("  Your choice: ").strip()

    if choice not in SERVICES:
        print("  [!] Invalid service selection.")
        pause()
        return

    session.selected_service_key = choice
    action()
    pause()


def my_subscriptions():
    clear()
    banner()
    user      = session.current_user
    all_subs  = Storage.load(Subscription.FILE)
    now       = datetime.now()
    user_subs = [s for s in all_subs if s.get("user_id") == user["id"]]

    if not user_subs:
        print("  You have no subscriptions yet.")
        return

    print(f"  {'Service':<15} {'Package':<12} {'Expires':<22} Status")
    divider()
    for s in user_subs:
        try:
            expiry = datetime.strptime(s["expiry"], "%Y-%m-%d %H:%M:%S")
            status = "✔  Active" if expiry > now else "✘  Expired"
            expiry_str = expiry.strftime("%Y-%m-%d %H:%M")
        except (ValueError, KeyError):
            expiry_str = "Unknown"
            status     = "?"
        print(f"  {s.get('service','?'):<15} {s.get('package','?'):<12} {expiry_str:<22} {status}")


def cancel_subscription():
    clear()
    banner()
    user     = session.current_user
    all_subs = Storage.load(Subscription.FILE)
    now      = datetime.now()

    # Collect (original_index, record) for active subs belonging to this user
    active = [
        (i, s) for i, s in enumerate(all_subs)
        if s.get("user_id") == user["id"]
        and datetime.strptime(s["expiry"], "%Y-%m-%d %H:%M:%S") > now
    ]

    if not active:
        print("  You have no active subscriptions to cancel.")
        return

    print("  ACTIVE SUBSCRIPTIONS\n")
    for display_num, (_, s) in enumerate(active, start=1):
        print(f"    [{display_num}]  {s['service']} — {s['package']}  "
              f"(expires {s['expiry']})")
    divider()

    choice = input("  Enter number to cancel (0 = back): ").strip()
    if choice == "0":
        return

    try:
        original_idx, record = active[int(choice) - 1]
    except (ValueError, IndexError):
        print("  [!] Invalid selection.")
        return

    confirm = input(
        f"\n  Cancel {record['service']} ({record['package']})? (yes/no): "
    ).strip().lower()

    if confirm != "yes":
        print("  No changes made.")
        return

    all_subs.pop(original_idx)
    Storage.save(Subscription.FILE, all_subs)
    logger.log(user["email"], f"Cancelled {record['service']} ({record['package']})")
    print("  ✔  Subscription cancelled successfully.")


def access_service():
   
    try:
        import importlib.util, pathlib
        spec = importlib.util.spec_from_file_location(
            "Automation",
            pathlib.Path(__file__).parent / "Automation.py" / " Automation.py"
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        automation = mod.ChatGPTAutomation(session, logger)
        automation.access_service()
    except FileNotFoundError:
        print("  [!] Automation module not found.")
    except Exception as e:
        print(f"  [!] Could not launch automation: {e}")
             
# Main loop 
# Runs the CLI until the user exits.

def main():
    clear()
    
    while True:
        clear()
        banner()
        status_bar()
        print()
        
        user = session.current_user
        if not user:
            logged_out_menu()
            print()
            choice = input("  Your choice: ").strip()
            print()
            if not handle_logged_out(choice):
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
