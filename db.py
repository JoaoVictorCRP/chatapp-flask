import sqlite3
from user import User
from werkzeug.security import generate_password_hash

con = sqlite3.connect('./backend/chat.db', check_same_thread=False)
cursor = con.cursor()

# cursor.execute("CREATE TABLE users(id INTEGER, username TEXT, email TEXT, password TEXT)")
res = cursor.execute("SELECT name FROM sqlite_master")

# HARD CODING ALERT...
def save_user(user):
    password_hash = generate_password_hash(user.password)
    cursor.execute(f"""
        INSERT INTO users(id, username, email, password) VALUES
            ('{user.id}', '{user.username}', '{user.email}', '{password_hash}')
        """
    )
    con.commit()

def get_user(username):
    user_data = cursor.execute(f'SELECT * FROM users WHERE username="{username}"')
    return user_data.fetchone() if user_data else None

# DEBUG ZONE :
# user = User('habia', 'habia@gmail', '123')
# save_user(user)
# print(f'\nDADOS INSERIDOS! \n {user.toString()}')

print(get_user('habia')[0])

# res = cursor.execute('SELECT * FROM users')
# print(res.fetchall())