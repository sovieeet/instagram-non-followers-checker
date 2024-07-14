import instaloader
import logging
import random
import time
import os
from excluded_accounts import excluded_accounts
from logging_config import setup_logging
from config import USER_AGENT, SESSION_FILE, SESSION_DIR

setup_logging()

def human_delay(min_seconds=3, max_seconds=10):
    """Introduce a random delay to simulate human behavior."""
    time.sleep(random.uniform(min_seconds, max_seconds))

def login_instaloader(L, username, password):
    session_file = os.path.join(SESSION_DIR, SESSION_FILE.format(username))
    logging.info('Logging into Instagram...')
    try:
        L.login(username, password)
        L.save_session_to_file(session_file)
        logging.info('Logged in and session saved successfully.')
        return True
    except Exception as e:
        logging.error(f'Failed to login: {e}')
        raise

def verify_session(L, username):
    try:
        profile = instaloader.Profile.from_username(L.context, username)
        list(profile.get_followers())
        return True
    except Exception as e:
        logging.error(f'Session verification failed: {e}')
        return False

def get_non_followers(L, username):
    try:
        logging.info('Fetching user profile...')
        profile = instaloader.Profile.from_username(L.context, username)
        logging.info(f'Logged in as: {profile.username}')
        
        human_delay()
        
        logging.info('Fetching followers...')
        followers = set(profile.get_followers())
        logging.info(f'Fetched {len(followers)} followers.')
        
        human_delay()
        
        logging.info('Fetching followees...')
        followees = set(profile.get_followees())
        logging.info(f'Fetched {len(followees)} followees.')
        
        followers_usernames = {follower.username for follower in followers}
        followees_usernames = {followee.username for followee in followees}
        
        non_followers = followees_usernames - followers_usernames
        
        logging.info('Manually excluded accounts:')
        for account in excluded_accounts:
            logging.info(account)
            if account not in followees_usernames:
                logging.warning(f'The excluded account {account} is not in the followees list.')
        
        non_followers -= set(excluded_accounts)
        
        logging.info(f'Identified {len(non_followers)} non-followers (excluding manually excluded accounts).')
        
        return list(non_followers)
    
    except instaloader.exceptions.TwoFactorAuthRequiredException:
        logging.info('Two-factor authentication required.')
        two_factor_code = input('Enter the 2FA code: ')
        L.two_factor_login(two_factor_code)
        L.save_session_to_file(os.path.join(SESSION_DIR, SESSION_FILE.format(username)))
        return get_non_followers(L, username)

if __name__ == "__main__":
    L = instaloader.Instaloader()
    L.context.user_agent = USER_AGENT

    username = input("Enter your Instagram username: ")
    session_file = os.path.join(SESSION_DIR, SESSION_FILE.format(username))
    
    if os.path.exists(session_file):
        logging.info(f'Trying to load session from file {session_file}...')
        try:
            L.load_session_from_file(username, session_file)
            logging.info('Session loaded successfully.')

            if not verify_session(L, username):
                logging.error('Session verification failed. Invalidating session.')
                os.remove(session_file)
                raise Exception('Session verification failed')
        except Exception as e:
            logging.error(f'Failed to load session from file: {e}')
            password = input("Enter your Instagram password: ")
            login_instaloader(L, username, password)
    else:
        password = input("Enter your Instagram password: ")
        login_instaloader(L, username, password)

    non_followers = get_non_followers(L, username)
    
    with open('non_followers.txt', 'w') as file:
        for user in non_followers:
            file.write(user + '\n')
    
    print("People you follow but don't follow you back:")
    for user in non_followers:
        print(user)
