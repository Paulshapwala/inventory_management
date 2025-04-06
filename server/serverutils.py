import sys
import os
# Add the parent directory containing 'app' to your path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import models
from sqlalchemy import select


class UserCRUD():
    @staticmethod
    def input_password():
        # will include logic to get user input that will generate a password
        return 'password'
    @staticmethod
    def createUser(session, name, admin):
       
        password = UserCRUD.input_password()
        user = models.User(username=name, isAdmin=admin)
        session.add(user)
        session.flush()
        code = models.Password(password_hash=password, user=user)
        session.add(code)
        session.commit()
        print(user.password.id)
        

