import os
import time
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from utils.decorators import require_login
from subscription.services import SERVICES
from subscription.subscribe import Subscription

# Test credentials 
TEST_EMAIL = "lucynjoka2025@gmail.com"
TEST_PASSWORD = "Lucy@7890q" 

class ServiceAutomation:

    def __init__(self, session, logger):
        self.session = session
        self.logger = logger
        self.subscription = Subscription(session, logger)

    @require_login
    def access_service(self, service_key):
        if service_key not in SERVICES:
            print(f"  [!] Unknown service key: '{service_key}'")
            return

        service = SERVICES[service_key]
        service_name = service["name"]
        service_url = service["url"]

        if not self.subscription.has_active_subscription(service_name):
            print("You do not have an active subscription for this service.")
            return

        user = self.session.current_user
        user_id = user["id"]
        email = user["email"]

        auth_file = f"data/auth_{user_id}_{service_name}.json"

        print(f"\nOpening {service_name}...")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, slow_mo=800)

            if os.path.exists(auth_file):
                print("Restoring saved session...")
                context = browser.new_context(storage_state=auth_file)
                page = context.new_page()
                page.goto(service_url)
                page.wait_for_load_state("networkidle")
                print("Logged in automatically using saved session.")
            else:
                context = browser.new_context()
                page = context.new_page()

                success = False
                try:
                    if service_name == "ChatGPT":
                        self._login_chatgpt(page)
                    elif service_name == "Grammarly":
                        self._login_grammarly(page)
                    elif service_name == "Ahrefs":
                        self._login_ahrefs(page)
                    elif service_name == "Envato Elements":
                        self._login_envato(page)
                    else:
                        print("Auto-login not configured for this service.")

                    success = True

                except PlaywrightTimeoutError as e:
                    print(f"  [!] Timed out: {e}")
                except Exception as e:
                    print(f"  [!] Auto-login failed: {e}")

                if not success:
                    input("Please complete login manually then press Enter...")

                # Save session after login
                context.storage_state(path=auth_file)
                print("Session saved! Next time you will be logged in automatically.")

            self.logger.log(email, f"Accessed {service_name}")
            input("\nPress Enter to return to CLI...")
            browser.close()

    # type into first visible matching input 
    def _fill(self, page, selectors, value):
        for sel in selectors:
            try:
                locator = page.locator(sel).first
                locator.wait_for(state="visible", timeout=5000)
                locator.click()
                locator.fill(value)
                print(f"    Filled: {sel}")
                return
            except Exception:
                continue
        raise Exception(f"Could not find any input with selectors: {selectors}")

    #click first visible matching element 
    def _click(self, page, selectors):
        for sel in selectors:
            try:
                locator = page.locator(sel).first
                locator.wait_for(state="visible", timeout=5000)
                locator.click()
                print(f"    Clicked: {sel}")
                return
            except Exception:
                continue
        raise Exception(f"Could not click any element with selectors: {selectors}")

    #  ChatGPT 
    def _login_chatgpt(self, page):
        print("Navigating to ChatGPT login...")
        page.goto("https://chatgpt.com/auth/login")
        page.wait_for_load_state("domcontentloaded")
        time.sleep(3)

        # Click "Log in" button on landing page
        print("  Clicking Log in button...")
        self._click(page, [
            "button:has-text('Log in')",
            "[data-testid='login-button']",
            "a:has-text('Log in')"
        ])
        page.wait_for_load_state("domcontentloaded")
        time.sleep(3)

        # Fill email 
        print("  Filling email...")
        self._fill(page, [
            "input[name='username']",        
            "input[type='email']",
            "input[id='username']",
            "#username"
        ], TEST_EMAIL)
        time.sleep(1)

        # Click Continue
        self._click(page, [
            "button[type='submit']:has-text('Continue')",
            "button:has-text('Continue')",
            "input[type='submit']"
        ])
        page.wait_for_load_state("domcontentloaded")
        time.sleep(3)

        # Fill password
        print("  Filling password...")
        self._fill(page, [
            "input[name='password']",
            "input[type='password']",
            "#password"
        ], TEST_PASSWORD)
        time.sleep(1)

        # Click Continue / Sign in
        self._click(page, [
            "button[type='submit']:has-text('Continue')",
            "button:has-text('Continue')",
            "button[type='submit']"
        ])
        page.wait_for_load_state("networkidle")
        time.sleep(4)

        print("Logged in to ChatGPT successfully!")

    #  Grammarly 
    def _login_grammarly(self, page):
        print("Navigating to Grammarly login...")
        page.goto("https://www.grammarly.com/signin")
        page.wait_for_load_state("domcontentloaded")
        time.sleep(3)

        print("  Filling email...")
        self._fill(page, [
            "input[name='email']",
            "input[type='email']",
            "input[placeholder*='email' i]"
        ], TEST_EMAIL)
        time.sleep(1)

        print("  Filling password...")
        self._fill(page, [
            "input[name='password']",
            "input[type='password']"
        ], TEST_PASSWORD)
        time.sleep(1)

        self._click(page, [
            "button:has-text('Log In')",
            "button[type='submit']"
        ])
        page.wait_for_load_state("networkidle")
        time.sleep(3)

        print("Logged in to Grammarly successfully!")

    #  Ahrefs 
    def _login_ahrefs(self, page):
        print("Navigating to Ahrefs login...")
        page.goto("https://app.ahrefs.com/user/login")
        page.wait_for_load_state("domcontentloaded")
        time.sleep(3)

        print("  Filling email...")
        self._fill(page, [
            "input[name='email']",
            "input[type='email']",
            "input[placeholder*='email' i]"
        ], TEST_EMAIL)
        time.sleep(1)

        print("  Filling password...")
        self._fill(page, [
            "input[name='password']",
            "input[type='password']"
        ], TEST_PASSWORD)
        time.sleep(1)

        self._click(page, [
            "button:has-text('Log in')",
            "button[type='submit']"
        ])
        page.wait_for_load_state("networkidle")
        time.sleep(3)

        print("Logged in to Ahrefs successfully!")

    # Envato Elements 
    def _login_envato(self, page):
        print("Navigating to Envato Elements login...")
        page.goto("https://account.envato.com/sign_in?to=elements")
        page.wait_for_load_state("domcontentloaded")
        time.sleep(3)

        print("  Filling username/email...")
        self._fill(page, [
            "input[name='username']",
            "input[id='user_username_or_email']",
            "input[type='email']",
            "input[placeholder*='username' i]"
        ], TEST_EMAIL)
        time.sleep(1)

        print("  Filling password...")
        self._fill(page, [
            "input[name='password']",
            "input[id='user_password']",
            "input[type='password']"
        ], TEST_PASSWORD)
        time.sleep(1)

        self._click(page, [
            "button:has-text('Sign in')",
            "input[type='submit']",
            "button[type='submit']"
        ])
        page.wait_for_load_state("networkidle")
        time.sleep(3)

        print("Logged in to Envato Elements successfully!")