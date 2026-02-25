

class Login:
    """Login class"""
    FILE = "users.json"  

    def __init__(self, session=None):
        self.session = session
        

    def login(self):
        """Login user by email and password"""
        print("\n=== Login ===")

        
        email = input("Enter email: ").strip()
        password = input("Enter password: ").strip()

       
        try:
            with open(self.FILE, "r") as file:
                users = eval(file.read())  
        except FileNotFoundError:
            users = []  

        
        user = next((u for u in users if u['email'] == email and u['password'] == password), None)

        if user:
            
            if self.session is not None:
                self.session.current_user = user
            print(f"Welcome {email}!")
            
        else:
            print("Invalid credentials")



if __name__ == "__main__":
    login_system = Login()
    login_system.login()
           