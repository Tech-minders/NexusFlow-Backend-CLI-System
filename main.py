"""
CLI entry point, menu loop and routing
1. Clear the terminal.
2. Print the  banner.
3. Show who is logged in .
4. Display the menu.
5. Read the user's choice.
6. Call the appropriate controller method.
7. Pause for 'Press Enter to continue'.
8. Loop back to step 1.

DYNAMIC MENU
Logged-out users see:  Sign Up, Log In, Exit
Logged-in users see:   Browse, Subscribe, History, Log Out, Exit

"""

import os
from auth.session import session


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

def menu():
    #Different options are shown depending on whether a user is logged in.
    user = session.get("user")
    print("  ─── MENU " + "─" * 38)
    if not user:
        # Unauthenticated: can only sign up or log in
        print("    [1]  Sign Up")
        print("    [2]  Log In")
    else:
        pass
# Main loop 

def main():
    clear()
    print("  Welcome to NexusFlow!")

    while True:
        clear()
        banner()
        status_bar()
        print()
        menu()
        print()


#Entry point 

if __name__ == "__main__":

    main()
