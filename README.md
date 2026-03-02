# **NexusFlow-Backend-CLI-System**
A command-line application that allows users to subscribe to and access premium online services (ChatGPT, Grammarly, Ahrefs, Envato Elements) through a unified interface with automated browser sessions via Playwright.

## **Features**

- **Account management** — sign up, log in, and log out with email/password authentication
- **Flexible packages** — subscribe by the hour, day, week, or month
- **Browser automation** — Playwright opens the chosen service and logs in automatically using a saved session
- **Session persistence** — browser state is saved after the first login; subsequent visits are instant
- **Subscription management** — view active subscriptions and cancel by ID
- **Activity logging** — every action (signup, login, subscribe, access, cancel) is timestamped and saved
- **Session timeout** — CLI sessions expire after 5 minutes of inactivity
 ---
## **Project Structure**
```
nexusflow/
├── main.py                      # Entry point and CLI menus
├── auth/
│   ├── auth.py                  # Signup, Login, Logout classes
│   └── session.py               # Session state management
├── subscription/
│   ├── subscribe.py             # Subscription logic (subscribe, list, cancel)
│   └── services.py              # Service and package definitions
├── automation/
│   └── automation.py               # Playwright browser automation
├── storage/
│   └── storage.py               # JSON file read/write utilities
├── utils/
│   ├── decorators.py            # @require_login decorator
│   └── logger.py                # Activity logger
└── data/                        # Auto-generated data directory
    ├── users.json
    ├── subscriptions.json
    ├── logs.json
    └── auth_<user_id>_<service>.json   # Saved browser sessions
```
---

## **Supported Services & Pricing (Kshs.)**

| Service          | Hourly | Daily | Weekly | Monthly |
|------------------|--------|-------|--------|---------|
| ChatGPT          | 30     | 100   | 500    | 2,000   |
| Grammarly        | 10     | 30    | 150    | 500     |
| Ahrefs           | 40     | 80    | 400    | 1,500   |
| Envato Elements  | 20     | 50    | 250    | 900     |

---

## Getting Started

**Clone the repository:**

```bash
git clone https://github.com/Tech-minders/NexusFlow-Backend-CLI-System.git
cd nexusflow
```

**Install dependencies:**

```bash
pip install playwright
playwright install chromium
```

**Run the app:**

```bash
python main.py
```

---

## Usage

When you run `main.py`, you'll see the NexusFlow banner and a menu based on your login state.

**Before logging in:**

```
[1]  Sign Up
[2]  Log In
[0]  Exit
```

**After logging in:**

```
[1]  Browse Services & Plans
[2]  Subscribe to a Plan
[3]  My Subscriptions
[4]  Access a Service
[5]  Cancel a Subscription
[0]  Log Out & Exit
```

### Typical flow

1. **Sign Up** — enter an email and password (confirmed). Passwords are SHA-256 hashed before storage.
2. **Log In** — authenticate with your credentials.
3. **Browse Services** — view all available services and their packages.
4. **Subscribe** — select a service and a package, confirm payment to activate.
5. **Access a Service** — select a service you're subscribed to. Playwright opens a Chromium browser. The first time, it logs in automatically (or prompts you to complete login manually if automation fails) and saves the session. Every visit after that is instant.
6. **Cancel** — list your active subscriptions and cancel one by its ID.
---

## Data Storage

All data is stored locally in the `data/` directory as JSON files:

- `users.json` — Registered user accounts (passwords stored as SHA-256 hashes)
- `subscriptions.json` — Subscription records with status and expiry dates
- `logs.json` — Timestamped log of all user actions
- `auth_<user_id>_<service>.json` — Saved Playwright browser sessions per user per service

The `data/` directory is created automatically on first run.

---

## Notes

- Only one active subscription per service is allowed per user at a time.
- The automation module includes login flows for all four supported services. If auto-login fails (e.g. due to a UI change), the user is prompted to complete login manually, after which the session is saved as normal.
- The `data/` directory and all JSON files are created automatically

---

## License

This project is for educational and personal use.
