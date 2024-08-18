import sqlite3
from user import User
from werkzeug.security import generate_password_hash

# Connecting to DB
con = sqlite3.connect('./chat.db', check_same_thread=False)
cursor = con.cursor()

# Save user to DB
def save_user(user:User):
    password_hash = generate_password_hash(user.password)
    cursor.execute("""
        INSERT INTO users(username, email, password) VALUES (?, ?, ?)
    """, (user.username, user.email, password_hash))
    con.commit()

# Get user data
def get_user(username:str):
    """Queries userdata of a given user, searching by the username.

        ~> Returns the queried user object (or None if the user does not exist)
    """
    cursor.execute('SELECT username, email, password FROM users WHERE username = ?', (username, ))
    user_data = cursor.fetchone() 

    return User(user_data[0],user_data[1], user_data[2]) if user_data else None

# Checks if user data is already on the database
def user_exists(**kwargs):

    # Checks if email already exists in database
    if 'email' in kwargs:
        cursor.execute('SELECT * FROM users WHERE email = ?', (kwargs['email'], ))
        return cursor.fetchone() is not None
    
    # Checks if username is already taken
    if 'username' in kwargs:
        cursor.execute("SELECT * FROM users WHERE username= ?", (kwargs['username'], ))
        return cursor.fetchone() is not None