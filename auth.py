# auth.py
import database
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    users = database.load_users()
    if username in users:
        return False
    users[username] = hash_password(password)
    database.save_users(users)
    return True

def login_user(username, password):
    users = database.load_users()
    hashed_pw = hash_password(password)
    return username in users and users[username] == hashed_pw

def is_admin(username, password):
    return username == "tanushri" and password == "tanushri123"
