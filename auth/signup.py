import uuid  

class Signup:
    """Signup class for new users"""
    FILE = "users.json"  

    def __init__(self, session=None):
        self.session = session
        

    def signup(self):
        """Create a new user account"""
        print("\n=== Signup ===")
        
        
        email = input("Enter email: ").strip()

        
        try:
            with open(self.FILE, "r") as file:
                users = eval(file.read())  
        except FileNotFoundError:
            users = []  

        
        if any(u['email'] == email for u in users):
            print("Email already exists!")
            return

        
        password = input("Enter password: ").strip()
        if len(password) < 6:
            print("Password too short! Must be at least 6 characters")
            return

        
        user = {
            "id": str(uuid.uuid4()),  
            "email": email,
            "password": password  
        }

        
        users.append(user)

        
        with open(self.FILE, "w") as file:
            file.write(str(users))  

        print("Signup successful!")
        


if __name__ == "__main__":
    s = Signup()
    s.signup()