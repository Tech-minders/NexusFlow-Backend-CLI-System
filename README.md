# **NexusFlow-Backend-CLI-System**
A command-line application that allows users to subscribe to and access premium online services (ChatGPT, Grammarly, Ahrefs, Envato Elements) through a unified interface with automated browser sessions via Playwright.

## **Features**

- User Authentication — Signup, login, and logout with SHA-256 password hashing
- Subscription Management — Subscribe to services with Hourly, Daily, Weekly, and Monthly packages
- Automated Browser Access — Launch and manage authenticated browser sessions via Playwright
- Session Persistence — Saves browser login state so users only log in manually once per service
- Activity Logging — All user actions are logged with timestamps to a JSON file
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

### Main Menu (Logged Out)
```
=== NexusFlow CLI ===
1. Signup
2. Login
0. Exit
```

### Main Menu (Logged In)
```
=== NexusFlow CLI ===
Logged in as: user@example.com
1. Select Service
2. Logout
0. Exit
```

**Subscribing** walks you through package selection and payment confirmation.

---

## Data Storage

All data is stored locally in the `data/` directory as JSON files:

- `users.json` — Registered user accounts (passwords stored as SHA-256 hashes)
- `subscriptions.json` — Subscription records with status and expiry dates
- `logs.json` — Timestamped log of all user actions
- `auth_<user_id>_<service>.json` — Saved Playwright browser sessions per user per service

The `data/` directory is created automatically on first run.

---

## Security Notes

- Passwords are hashed using SHA-256 before storage — plain-text passwords are never saved.
- Browser session files are stored locally and tied to a specific user ID and service.
- No payment processing is integrated; the payment step is simulated via CLI confirmation.

---

## License

This project is for educational and personal use.
