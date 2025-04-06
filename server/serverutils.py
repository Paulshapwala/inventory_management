import sys
import os
# Add the parent directory containing 'app' to your path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import models
from server.setup import engine
from sqlalchemy import select, delete, insert, update
from sqlalchemy.orm import Session


class UserCRUD():
    @staticmethod
    def input_password():
        # will include logic to get user input that will generate a password
        return 'password'
    @staticmethod
    def createUser(session:Session, name:str, admin:bool):
       
        password = UserCRUD.input_password()
        user = models.User(username=name, isAdmin=admin)
        session.add(user)
        session.flush()
        code = models.Password(password_hash=password, user=user)
        session.add(code)
        session.commit()
        print(f"user {name} added")
    @staticmethod
    def get_id(id_list:list):
        
        # will include logic to ask for id if multiple matches are found
        id =input(f"choose an id from:{id_list} ")
        return id

    @staticmethod
    def delete_user(session:Session,name:str, id:int=None):
        stmt = select(models.User).where(models.User.username==name)
        users= session.scalars(stmt).all()
        if not users:
            print(f"{name} does not exist")
            return
        elif len(users) > 1:
            id_list = []
            for user in users:
                id_list.append(user.id)
            id = UserCRUD.get_id(id_list)
            stmt = session.query(models.User).filter_by(id=id).first()
            
        else:
            stmt = session.query(models.User).filter_by(username=name).first()
            
        print(stmt)
        print(id)
        session.delete(stmt)
        session.commit()

