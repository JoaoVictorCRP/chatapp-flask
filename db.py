import sqlite3
from werkzeug.security import generate_password_hash

con = sqlite3.connect('./backend/chat.db')
cursor = con.cursor()

# cursor.execute("CREATE TABLE users(username TEXT, email TEXT, password TEXT)")
res = cursor.execute("SELECT name FROM sqlite_master") # retorna nome das tabelas criadas


def save_user(username, email, password):
    password_hash = generate_password_hash(password)
    cursor.execute(f"""
        INSERT INTO users(username, email, password) VALUES
            ('{username}', '{email}', '{password_hash}')
        """
    )
    con.commit()

# save_user('habia', 'habia@gmail.com', '123')
# res = cursor.execute('SELECT * FROM users')
print(res.fetchall())