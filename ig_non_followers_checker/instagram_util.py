import instaloader
import logging
from excluded_accounts import excluded_accounts
from logging_config import setup_logging

setup_logging()

def get_non_followers(username, password):
    logging.info('Logging into Instagram...')
    L = instaloader.Instaloader()
    
    L.login(username, password)
    
    logging.info('Fetching user profile...')
    profile = instaloader.Profile.from_username(L.context, username)
    logging.info(f'Logged in as: {profile.username}')
    
    logging.info('Fetching followers...')
    followers = set(profile.get_followers())
    logging.info(f'Fetched {len(followers)} followers.')
    
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
