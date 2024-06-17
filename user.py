class User:
    def __init__(self, username, email, password) -> None:
        self.username = username
        self.email = email
        self.password = password

    @staticmethod
    def is_authenticated(self):
        return True
    
    @staticmethod
    def is_activated(self):
        return True
    
    @staticmethod
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return self.username