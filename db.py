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

    # FIXME: MAYBE I COULD JUST ADD ALL VERIFICATION STEP RIGHT HERE

    return User(user_data[0],user_data[1], user_data[2]) if user_data else None

# Checks if user data is already on the database
def user_exists(**kwargs):
    # Checks if email already exists in database
    
    if kwargs.get('email'):
        user_data = cursor.execute(f'SELECT * FROM users WHERE email="{kwargs.get('email')}"')
        user_data = user_data.fetchone()
        return True if user_data else False
    
    # Checks if username is already taken
    if kwargs.get('username'):
        user_data = cursor.execute(f'SELECT * FROM users WHERE username="{kwargs.get('username')}"')
        user_data = user_data.fetchone()
        return True if user_data else False