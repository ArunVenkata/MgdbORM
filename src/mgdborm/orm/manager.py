import enum
import warnings
import certifi

import pymongo
from pymongo.collection import Collection


class MgdbClass:
    """
    Usage:
    Mgdb.database("<database_name>").collection("<name>").<any mongodb collection function available in pymongo>
    """

    _query = None

    def __init__(self, mongo_url) -> None:
        self.url = mongo_url

    def __get_mgdb_client(self):
        mongo_client = pymongo.MongoClient(self.url, tlsCAFile=certifi.where())
        return mongo_client

    def collection(self, collection_name: str):
        if self._query is None:
            raise ValueError("Database Name not defined")
        return self._query[collection_name]
    
    def database(self, name: str):
        if not isinstance(name, str):
            raise ValueError(f"{name} is not a valid database name")
        self._query = self._database(name)
        return self

    def _database(self, name):
        return self.__get_mgdb_client()[name]


class MgdbManager:
    __collection_class = None
    __default_db_name = None
    __mandatory_settings = {}
    __settings = {"strictmode": True}
    def __init__(self, mongo_url, default_db_name: str, settings={"strictmode": True}):
        if not isinstance(default_db_name, str):
            raise ValueError("Database name must be a string!")

        if not isinstance(mongo_url, str):
            raise ValueError("Mongo Url must be a string!")

        self.__default_db_name = default_db_name
        self.mongo_url = mongo_url
        self._mgdb = MgdbClass(self.mongo_url)

    def update_settings(self, settings:dict):
        self.__settings = {**self.__settings, **settings, **self.__mandatory_settings}
        return self.__settings

    def __checks(self):
        """Class level error checks"""
        if self.__collection_class is None:
            if self.__settings.get("strictmode")==True:
                raise ValueError(
                    "Collection class has not been registered. Call register_collection_class first!"
                )
            warnings.simplefilter("always", SyntaxWarning)
            warnings.warn(
                f"Collection class is missing, Please use collection class. Refer to https://github.com/ArunVenkata/MgdbORM/blob/master/README.md",
                category=SyntaxWarning,
                stacklevel=2
            )
            warnings.simplefilter("default", SyntaxWarning)
        
        if self.__default_db_name is None:
            raise ValueError("Default Database name has not been specified")

    def register_collection_class(self, class_ref):
        if not issubclass(class_ref, enum.Enum):
            raise ValueError("Class type not valid, class must inherit from Enum!")
        self.__collection_class = class_ref

    def get(self, collection_name: __collection_class) -> Collection:

        self.__checks()

        
        if isinstance(collection_name, self.__collection_class):
            collection_name = collection_name.value

        return self._mgdb.database(self.__default_db_name).collection(
            collection_name
        )


class MandateMgdbManager:
    mgdb_manager = None

    def __init__(self, *args, **kwargs):
        if not isinstance(kwargs.get("mgdb_manager_instance"), MgdbManager):
            raise ValueError(
                "MgdbManager instance Missing!\nAssign mgdb_manager_instance to be an instance of MgdbManager!"
            )
        self.mgdb_manager: MgdbManager = kwargs.get("mgdb_manager_instance")


__all__ = ("MgdbClass", "MgdbManager", "MandateMgdbManager")