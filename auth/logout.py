
class Logout:
    """Logout class"""

    def __init__(self, session=None):
        self.session = session
        

    def logout(self):
        """Logout current user"""
        if self.session and getattr(self.session, "current_user", None):
            email = self.session.current_user['email']
            self.session.current_user = None
            print("Logged out successfully!")
            
        else:
            print("No user logged in")



class Session:
    current_user = None



if __name__ == "__main__":
    session = Session()
    session.current_user = {"email": "test@example.com"}  
    logout_system = Logout(session)
    logout_system.logout()
          