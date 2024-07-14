import os

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
SESSION_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sessions')
if not os.path.exists(SESSION_DIR):
    os.makedirs(SESSION_DIR)
SESSION_FILE = os.path.join(SESSION_DIR, "session-{}.instaloader")
