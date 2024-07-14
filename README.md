# Instagram Non-Followers Checker

This tool allows you to identify which accounts you follow on Instagram that do not follow you back. It uses the instaloader library to fetch your followers and followees and then compares these lists. You can also manually exclude certain accounts from being listed as non-followers.

## Features
- **Log into Instagram**: Automatically log into your Instagram account.
- **Fetch Followers and Followees**: Retrieve the list of your followers and the accounts you follow.
- **Identify Non-Followers**: Compare the lists to identify accounts that do not follow you back.
- **Manual Exclusion**: Exclude specified accounts from the non-followers list.

## Setup

### 1. Clone the repository
```git
git clone https://github.com/sovieeet/instagram-non-followers-checker.git
cd instagram-non-followers-checker
```

### 2. Create and Activate Virtual Environment (optional but recommended):
```python
python -m venv .venv
source .venv/Scripts/activate  # On Linux/UNIX systems, use `.venv\bin\activate`
```

### 3. Install Dependencies:

```python
pip install -r requirements.txt
```

**NOTE: If you have Make installed, you can use `make install` instead**

### 4. Configure Credentials:

Set up the `config.json` file in the `credentials` folder with your credentials

```json
{
    "username": "your_instagram_username",
    "password": "your_instagram_password"
}
```

### 5. Add Accounts to Exclude

In `excluded_accounts.py`, list the accounts you want to manually exclude from the non-followers list:

```python
excluded_accounts = ["account1", "account2", "account3"]
```

## Usage

Run the script to generate the list of non-followers:

```bash
python ig_non_followers_checker/main.py
```
**NOTE: If you have Make installed, you can use `make run` instead**

## Important Note

### This script does not store any credentials. Your Instagram username and password are used only for logging into your account and fetching the necessary data during the execution of the script.