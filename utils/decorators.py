from functools import wraps

def require_login(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):

        # Check if session has timed out
        if self.session.is_expired():
            print("\n  [!] Your session has expired due to inactivity. Please log in again.")
            self.session.expire()
            return

        if not self.session.current_user:
            print("You must login first.")
            return

        # Reset activity timer on every action
        self.session.update_activity()

        return func(self, *args, **kwargs)

    return wrapper