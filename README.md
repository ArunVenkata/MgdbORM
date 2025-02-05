# MgdbORM

## What is this ?
This is some python code to help keep your mongo collections and databases organised.

Any Contributions are welcome!

## Usage

```python

import enum
from mgdborm.orm import MgdbManager

# Define an Enum for Collections
class MyCollections(enum.Enum):
    _DB_NAME = "my_database"
    USERS = "users"
    ORDERS = "orders"

# Initialize MgdbManager with custom settings if needed
manager = MgdbManager(_settings={"strictmode": True})

# Register the collection class
manager.register_collection_class(MyCollections)

# Query the 'users' collection
users_collection = manager.query(MyCollections.USERS)

# Perform operations on the 'users' collection
user_data = users_collection.find_one({"username": "johndoe"})
print(user_data)
```
