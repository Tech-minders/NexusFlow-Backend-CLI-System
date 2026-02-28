#Store logged-in user and selected service for the current CLI session

class Session:
    def __init__(self):
        self.current_user = None
        self.selected_service_key = None


   