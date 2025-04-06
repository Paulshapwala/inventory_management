import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import serverutils, setup, models
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
engine = setup.engine
Base = setup.Base
# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
# serverutils.UserCRUD.createUser(session, "Paul", True)


serverutils.UserCRUD.delete_user(session,"Paul")
