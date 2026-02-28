import uuid
import hashlib  
from storage.storage import Storage 
from utils.logger import Logger  


class Auth:
    

    FILE = "data/users.json"  

    def __init__(self, session, logger: Logger):
        self.session = session  
        self.logger = logger  

    def hash_password(self, password):
        
        return hashlib.sha256(password.encode()).hexdigest()  
    def valid_email(self, email):
        return "@" in email and "." in email


        
class Signup(Auth):
    

    def signup(self):
        print("\n=== Signup ===")
        email = input("Enter email: ").strip()

        
        if not self.valid_email(email):
            print("Invalid email format!")
            return
        
        users = Storage.load(self.FILE)
        if any(user["email"] == email for user in users):
            print("Email already exists!")
            return


        password = input("Enter password: ").strip()
        confirm_password = input("Confirm password: ").strip()

        
        if password != confirm_password:
            print("Passwords do not match!")
            return

        
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
    

    def login(self):
        print("\n=== Login ===")
        email = input("Enter email: ").strip()

        
        if not self.valid_email(email):
            print("Invalid email format!")
            return

        password = input("Enter password: ").strip()
        hashed_password = self.hash_password(password)
        users = Storage.load(self.FILE)


        user_found = next((u for u in users if u["email"] == email and u["password"] == hashed_password), None)
        if user_found:
            self.session.current_user = user_found
            print(f"Welcome {email}!")
            self.logger.log(email, "Logged in")
        else:
            print("Invalid credentials")


class Logout(Auth):
    

    def logout(self):
        
        if self.session.current_user:
            email = self.session.current_user["email"]
            self.session.current_user = None
            print("Logged out successfully!")
            self.logger.log(email, "Logged out")
        else:
            print("No user logged in")