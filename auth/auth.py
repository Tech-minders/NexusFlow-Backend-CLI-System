import uuid
import hashlib  # Used for password hashing
from storage.storage import Storage  # Handles JSON storage
from Utils.logger import Logger  # Logs user actions


class Auth:
    # Parent authentication class with shared logic

    FILE = "data/users.json"  # Common storage file

    def __init__(self, session, logger: Logger):
        self.session = session  # Store session
        self.logger = logger  # Store logger

    def hash_password(self, password):
        # Hash a password using SHA256
        return hashlib.sha256(password.encode()).hexdigest()  # Return hashed password

    def valid_email(self, email):
        # Check if email contains @ and .
        if "@" in email and "." in email:
            return True
        else:
            return False
        
class Signup(Auth):
    # Sign up new users

    def signup(self):
        print("\n=== Signup ===")
        email = input("Enter email: ").strip()

        # Validate email
        if not self.valid_email(email):
            print("Invalid email format!")
            return
        #Create a storage instance
        users = Storage.load(self.FILE)

        # Check if email already exists
        email_exists = False
        for user in users:
            if user["email"] == email:
                email_exists = True
                break

        if email_exists:
            print("Email already exists!")
            return

        password = input("Enter password: ").strip()
        confirm_password = input("Confirm password: ").strip()

        # Check if passwords match
        if password != confirm_password:
            print("Passwords do not match!")
            return

        # Create new user with hashed password
        user = {
            "id": str(uuid.uuid4()),
            "email": email,
            "password": self.hash_password(password)
        }

        users.append(user)
        Storage.save(self.FILE, users)

        print("Signup successful!")
        self.logger.log(email, "Signed up")

class Login(Auth):
    # Login existing users

    def login(self):
        print("\n=== Login ===")
        email = input("Enter email: ").strip()

        # Validate email
        if not self.valid_email(email):
            print("Invalid email format!")
            return

        password = input("Enter password: ").strip()
        hashed_password = self.hash_password(password)

        users = Storage.load(self.FILE)

        # Search for matching user
        user_found = None
        for user in users:
            if user["email"] == email:
                if user["password"] == hashed_password:
                    user_found = user
                    break

        if user_found:
            self.session.current_user = user_found
            print(f"Welcome {email}!")
            self.logger.log(email, "Logged in")
        else:
            print("Invalid credentials") 
class Logout(Auth):
    # Logout current user

    def logout(self):
        # Check if user is logged in
        if self.session.current_user:
            email = self.session.current_user["email"]
            self.session.current_user = None
            print("Logged out successfully!")
            self.logger.log(email, "Logged out")
        else:
            print("No user logged in")