#Store logged-in user and selected service for the current CLI session
from datetime import datetime,timedelta

class Session:
    TIMEOUT_MINUTES = 5
    def __init__(self):
        self.current_user = None
        self.selected_service_key = None
        self.last_activity = None
    def update_activity(self):
        self.last_activity = datetime.now()

    def is_expired(self):
        if not self.current_user:
            return False
        if not self.last_activity:
            return True
        return datetime.now() - self.last_activity > timedelta(minutes=self.TIMEOUT_MINUTES)
    
    def expire(self):
        self.current_user = None
        self.selected_service_key = None
        self.last_activity = None
  

   