# decorators:

import functools    
import time           
from datetime import datetime 
from auth.session import session

# DECORATOR 1: @require_login
# Checks if session["user"] has a value
# If NO  -> prints "ACCESS DENIED" and stops.
# If YES -> lets the real function run normally

def require_login(func):
    
    @functools.wraps(func) # makes sure the wrapped function keeps its original name.
    def wrapper(*args, **kwargs):
        if session["user"] is None:
            print(" ACCESS DENIED! Please log in first.")
            return None
        return func(*args, **kwargs)
    return wrapper


# DECORATOR 2: @log_action
#Prints a timestamped log line before the function runs.

def log_action(action_name):
    
    def decorator(func):   # receives the actual function being decorated
        @functools.wraps(func)
        # runs every time the decorated function is called
        def wrapper(*args, **kwargs):
            # check who is logged in 
            user      = session.get("user")
            email     = user["email"] if user else "anonymous"
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Print the log line BEFORE the function runs
            print(f"  [{timestamp}] {email} -> {action_name}")

            # Now run the real function
            return func(*args, **kwargs)
        return wrapper
    return decorator  

# DECORATOR 3: @handle_errors
# Runs the function inside a try/except block

def handle_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # Try to run the function normally
            return func(*args, **kwargs)

        except FileNotFoundError as e:
            print(f"ERROR! File not found: {e}")
            return None

        except Exception as e:
            print(f"ERROR! Something went wrong: {e}")
            return None
    return wrapper

# DECORATOR 4: @timer
# Records the time just before the function runs
# Records the time just after it finishes
# Prints how many seconds it took

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start  = time.perf_counter()      
        result = func(*args, **kwargs)  
        end  = time.perf_counter()   

        # Print elapsed time rounded to 4 decimal places
        print(f"  [TIMER] {func.__name__} -> {end - start:.4f}s")

        return result   # pass back whatever the function returned
    return wrapper


# DECORATOR 5: @confirm_action
# Shows the question and waits for the user to type yes or no
# If they type "yes" -> the function runs
# Anything else -> prints "Cancelled." 


def confirm_action(prompt="Are you sure?"):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Ask the question , strip spaces, make lowercase for comparison
            answer = input(f"  {prompt} (yes/no): ").strip().lower()

            if answer != "yes":
                print("  Cancelled.")
                return None

            return func(*args, **kwargs)
        return wrapper
    return decorator  
