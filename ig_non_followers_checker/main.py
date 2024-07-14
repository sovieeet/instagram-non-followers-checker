import instaloader
import logging
import os
import getpass
from instagram_util import get_non_followers, login_instaloader, verify_session
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
    session_file = os.path.join(SESSION_DIR, SESSION_FILE.format(username)) if username else None
    session_loaded = False

    if session_file and os.path.exists(session_file):
        logging.info(f'Trying to load session from file {session_file}...')
        try:
            L.load_session_from_file(username, session_file)
            logging.info('Session loaded successfully.')

            if not verify_session(L, username):
                logging.error('Session verification failed. Invalidating session.')
                os.remove(session_file)
                session_loaded = False
            else:
                session_loaded = True
        except Exception as e:
            logging.error(f'Failed to load session from file: {e}')
            session_loaded = False

    if not session_loaded:
        username = input("Enter your Instagram username: ")
        password = getpass.getpass("Enter your Instagram password: ")
        try:
            login_instaloader(L, username, password)
        except Exception as e:
            logging.error(f'Failed to login: {e}')
            return  # Detener el script si falla el inicio de sesión

    non_followers = get_non_followers(L, username)

    with open('non_followers.txt', 'w') as file:
        for user in non_followers:
            file.write(user + '\n')

    print("People you follow but don't follow you back:")
    for user in non_followers:
        print(user)

if __name__ == "__main__":
    main()
