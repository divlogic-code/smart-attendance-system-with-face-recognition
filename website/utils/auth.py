import json
from werkzeug.security import check_password_hash

def load_users():
    with open('users.json') as f:
        return json.load(f)

def authenticate(roll_number, password):
    users = load_users()
    user = users.get(roll_number)
    if user and check_password_hash(user['password'], password):
        return user
    return None
