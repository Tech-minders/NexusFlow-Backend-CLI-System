

class Session:
    # Keep track of the current logged-in user

    def __init__(self):
        self.current_user = None
        self.selected_service_key = None   



if __name__ == "__main__":
    session = Session()
    print("Current user:", session.current_user) 

    #Store logged-in user and selected service for the current CLI session


   