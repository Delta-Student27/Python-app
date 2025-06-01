# database.py
import json
import os

VOTES_DB = 'votes.json'
USERS_DB = 'users.json'
VOTED_USERS_DB = 'voted_users.json'

def load_votes():
    if not os.path.exists(VOTES_DB):
        return {}
    with open(VOTES_DB, 'r') as f:
        return json.load(f)

def save_votes(data):
    with open(VOTES_DB, 'w') as f:
        json.dump(data, f, indent=4)

def load_users():
    if not os.path.exists(USERS_DB):
        return {}
    with open(USERS_DB, 'r') as f:
        return json.load(f)

def save_users(data):
    with open(USERS_DB, 'w') as f:
        json.dump(data, f, indent=4)

def load_voted_users():
    if not os.path.exists(VOTED_USERS_DB):
        return []
    with open(VOTED_USERS_DB, 'r') as f:
        return json.load(f)

def save_voted_users(data):
    with open(VOTED_USERS_DB, 'w') as f:
        json.dump(data, f, indent=4)

def reset_all():
    save_votes({})
    save_users({})
    save_voted_users([])
