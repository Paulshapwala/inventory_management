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
        # TODO map this with frontend:include logic to get user input that will generate a password
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
        
        # TODO map this with widget: to include logic to ask for id if multiple matches are found
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

        session.delete(stmt)
        session.commit()


class ProductCRUD():
    @staticmethod
    def get_product():
        # TODO map this with button
        return {"name":"oranges", "category":"fruits" ,"quantity":5 ,"price":5.6,}
    

    @staticmethod
    def get_id(id_list:list):
        # TODO map to front end
        id =input(f"choose an id from:{id_list} ")
        return id

        
    @staticmethod
    def add_product(session:Session):
        # TODO make data transfer to backend more secure
        item = ProductCRUD.get_product()
        product = models.Product(name=item["name"],category=item["category"], 
                                 quantity=item["quantity"],price=item["price"])
        session.add(product)
        session.commit()
        print("Item added")
    class Modification:
        @staticmethod
        def delete_product(session:Session,name:str, id:int=None):
            stmt = select(models.Product).where(models.Product.name==name)
            products = session.scalars(stmt).all()
            if not products:
                print(f"{name} does not exist")
                return
            elif len(products) > 1:
                id_list = []
                for product in products:
                    id_list.append(product.id)
                id = ProductCRUD.get_id(id_list)
                stmt = session.query(models.Product).filter_by(id=id).first()
                
            else:
                stmt = session.query(models.User).filter_by(username=name).first()

            session.delete(stmt)
            session.commit()


