import instaloader
import logging
import os
from instagram_util import get_non_followers, login_instaloader
from config import USER_AGENT, SESSION_FILE, SESSION_DIR

def get_username_from_session_file():
    session_files = [f for f in os.listdir(SESSION_DIR) if f.startswith("session-") and f.endswith(".instaloader")]
    if session_files:
        session_file = session_files[0]
        username = session_file[len("session-"):-len(".instaloader")]
        return username
    return None

def main():
    L = instaloader.Instaloader()
    L.context.user_agent = USER_AGENT

    username = get_username_from_session_file()
    if username:
        logging.info(f'Found session file for username: {username}')
    else:
        logging.info("Session file not found. Requesting username.")
        username = input("Enter your Instagram username: ")

    session_file = os.path.join(SESSION_DIR, SESSION_FILE.format(username))
    session_loaded = False
    if os.path.exists(session_file):
        logging.info(f'Trying to load session from file {session_file}...')
        try:
            L.load_session_from_file(username, session_file)
            logging.info('Session loaded successfully.')
            session_loaded = True
        except Exception as e:
            logging.error(f'Failed to load session from file: {e}')

    if not session_loaded:
        logging.info("Session not loaded. Requesting password.")
        password = input("Enter your Instagram password: ")
        login_instaloader(L, username, password)

    non_followers = get_non_followers(L, username)

    with open('non_followers.txt', 'w') as file:
        for user in non_followers:
            file.write(user + '\n')

    print("People you follow but don't follow you back:")
    for user in non_followers:
        print(user)

if __name__ == "__main__":
    main()
