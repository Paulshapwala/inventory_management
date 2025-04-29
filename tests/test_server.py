import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import serverutils, setup, models
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
engine = setup.engine
Base = setup.Base
# Base.metadata.drop_all(engine)
# Base.metadata.transactionItems.drop(engine)
# Base.metadata.transactions.drop(engine)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
# serverutils.UserCRUD.createUser(session, "Paul", True)
# serverutils.ProductCRUD.add_product(session)

# serverutils.UserCRUD.delete_user(session,"Paul")
# serverutils.ProductCRUD.Modification.delete_product(session, "apples")
# serverutils.ProductCRUD.Modification.change_quantity(session,"banana",new_quantity=17)
# serverutils.ProductCRUD.Modification.change_price(session, "banana", 28.9)
serverutils.Transaction.create_transaction(session,6,[(11,2)])