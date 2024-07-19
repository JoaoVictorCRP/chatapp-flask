import sqlite3
from user import User
from werkzeug.security import generate_password_hash

# Connecting to DB
con = sqlite3.connect('./backend/chat.db', check_same_thread=False)
cursor = con.cursor()

# Save user to DB
def save_user(user:User):
    password_hash = generate_password_hash(user.password)
    cursor.execute(f"""
        INSERT INTO users(username, email, password) VALUES
            ('{user.username}', '{user.email}', '{password_hash}')
        """
    )
    con.commit()

# Get user data
def get_user(username:str):
    """Queries userdata of a given user, searching by the username.

        ~> Returns the queried user object
    """
    user_data = cursor.execute(f'SELECT * FROM users WHERE username="{username}"')
    user_data = user_data.fetchone() 
    return User(user_data[0],user_data[1], user_data[2]) if user_data else None

# Check if email already exists in database
def email_exists(email:str):
    user_data = cursor.execute(f'SELECT * FROM users WHERE email="{email}"')
    user_data = user_data.fetchone()
    return True if user_data else False
