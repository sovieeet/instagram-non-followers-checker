import json
import os
from ig_non_followers_checker.instagram_util import get_non_followers

def load_credentials(filename):
    with open(filename, 'r') as file:
        return json.load(file)

if __name__ == "__main__":
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'credentials', 'config.json')
    
    credentials = load_credentials(config_path)
    username = credentials['username']
    password = credentials['password']
    
    non_followers = get_non_followers(username, password)
    
    with open('non_followers.txt', 'w') as file:
        for user in non_followers:
            file.write(user + '\n')
    
    print("People you follow but don't follow you back:")
    for user in non_followers:
        print(user)
