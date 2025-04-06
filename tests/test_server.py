import sys
import os
# Add the parent directory containing 'app' to your path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now use regular imports
from server import serverutils, setup, models
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

engine = setup.engine
Session = sessionmaker(bind=engine)
session = Session()
serverutils.UserCRUD.createUser(session, "steve", False)
stmt = select(models.User)
print(list(session.execute(stmt)))