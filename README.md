# MgdbORM

## What is this ?
This is some python code to help keep your mongo collections and databases organised.

Any Contributions are welcome!

## Usage

```python

# Create a collection Class to keep track of Collections
from enum import Enum
class AuthCollections(Enum):
    USERS = 'users'
    ACCESS_TOKEN = 'access_token'

# For a database which stores authentication related data
mgdb_manager = MgdbManager(mongo_url=os.environ("URL"), "auth")
mgdb_manager.register_collections_class(AuthCollections)


# Create your own custom class for Crud operations on Auth Db and inherit form MandateMgdbManager

class AuthDbManager(MandateMgdbManager):

    def create_user(self, name, email):
        # self.mgdb_manager will be available through inherited class
        # insert_one is a pymongo function, you can use any pymongo function
        # .get will get the collection instance returned by pymongo
        return self.mgdb_manager.get(AuthCollections.USERS).insert_one(dict(name=name, email=email))


# Pass auth_db as mgdb_manager_instance to the AuthDbManager class
auth_db = AuthDbManager(mgdb_manager_instance=mgdb_manager)

# Use as required
user_details = auth_db.create_user(name="John Doe", email="johndoe@example.com")
```
