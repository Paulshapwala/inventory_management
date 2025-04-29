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
        return {"name":"banana", "category":"fruits" ,"quantity":5 ,"price":5.6,}
    

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
        def _get_product_to_modify(session: Session, name: str, id: int = None):
            """This is a useful get product method for modification functions"""
            stmt = select(models.Product).where(models.Product.name == name)
            products = session.scalars(stmt).all()
            
            if not products:
                print(f"{name} does not exist")
                return None
            
            # If multiple products found with the same name
            if len(products) > 1:
                id_list = [product.id for product in products]
                
                # Check if the provided ID is valid for the products with this name
                if id is not None and id in id_list:
                    return session.get(models.Product, id)
                else:
                    # If no ID provided or ID invalid, ask for ID selection
                    selected_id = ProductCRUD.get_id(id_list)
                    return session.get(models.Product, selected_id)
            else:
                # If only one product found
                return products[0]
        @staticmethod
        def delete_product(session:Session,name:str, id:int=None):
            product = ProductCRUD.Modification._get_product_to_modify(session,name,id)
            session.delete(product)
            session.commit()
            print(f"{name} deleted!")

        @staticmethod
        def change_quantity(session: Session, name: str, new_quantity: int,id: int = None):
            product = ProductCRUD.Modification._get_product_to_modify(session,name,id)
            product.quantity = new_quantity
            session.commit()
            print(f"Price for '{name}' updated to {new_quantity}")

        @staticmethod
        def change_price(session:Session, name:str, new_price:float, id:int = None):
            product = ProductCRUD.Modification._get_product_to_modify(session,name,id)
            product.price = new_price
            session.commit()
            print(f"Price for '{name}' updated to {new_price}")


class Transaction():
    @staticmethod
    def create_transaction(session: Session, user_id: int, item_list: list[tuple]):
        """
        Creates a transaction with multiple items for a user.
        
        Args:
            session: Database session
            user_id: ID of the user making the purchase
            item_list: List of tuples (product_id, quantity)
            
        Returns:
            The created transaction object
            
        Raises:
            ValueError: If any product has insufficient quantity
        """
        # Validate quantities first before making any changes
        insufficient_items = []
        
        for product_id, quantity in item_list:
            if not isinstance(quantity, int) or quantity <= 0:
                raise ValueError(f"Invalid quantity {quantity} for product {product_id}. Quantity must be a positive integer.")
                
            product = session.get(models.Product, product_id)
            if product.quantity < quantity:
                insufficient_items.append((product_id, product.name, product.quantity, quantity))
        
        # If any items have insufficient quantity, raise an error with details
        if insufficient_items:
            error_msg = "Cannot complete transaction due to insufficient inventory:\n"
            for prod_id, name, available, requested in insufficient_items:
                error_msg += f"- Product ID {prod_id} ({name}): Requested {requested}, Available {available}\n"
            raise ValueError(error_msg)
            
        try:
            # Create transaction record
            transaction = models.Transaction(userId=user_id)
            session.add(transaction)
            
            # Process each item
            for product_id, quantity in item_list:
                # Get the product and its current price
                product = session.get(models.Product, product_id)
                
                # Create transaction item
                transaction_item = models.TransactionItem(
                    productId=product_id,
                    priceAtTime=product.price,
                    quantity=quantity
                )
                
                # Add item to transaction
                transaction.items.append(transaction_item)
                
                # Update product inventory
                product.quantity -= quantity
            
            # Commit all changes to database
            session.commit()
            return transaction
            
        except Exception as e:
            # Roll back transaction in case of any error
            session.rollback()
            raise RuntimeError(f"Transaction failed: {str(e)}")