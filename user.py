import uuid # Random ID generator
from werkzeug.security import check_password_hash

class User:
    def __init__(self, username, email, password) -> None:
        self.id = uuid.uuid1()
        self.username = username
        self.email = email
        self.password = password

    @staticmethod
    def is_authenticated(self):
        # TODO: Auth Logic
        return True
    
    @staticmethod
    def is_active(self):
        return True
    
    @staticmethod
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return self.id
    
    def toString(self): # Debugging purpose
        return f'id: {self.id}\
        username: {self.username}\
        email: {self.email}\
        password: {self.password}\
        '
    
def check_user_password(hashedPassword, password_input):
    return check_password_hash(hashedPassword, password_input)


# user = User('Joao','joao@gmail.com','123')
# print(user.toString())