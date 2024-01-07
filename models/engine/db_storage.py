#!/usr/bin/python3
"""
This module contains the DBStorage class
"""
from sqlalchemy import create_engine
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy.orm import sessionmaker, scoped_session
import os
from models.base_model import Base


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        """
        Create the engine (self.__engine)
        The engine must be linked to the MySQL database and user
        created before:
        dialect: mysql
        driver: mysqldb
        """
        self.__engine = create_engine(
                'mysql+mysqldb://{}:{}@{}/{}'
                .format(os.getenv('HBNB_MYSQL_USER'),
                        os.getenv('HBNB_MYSQL_PWD'),
                        os.getenv('HBNB_MYSQL_HOST'),
                        os.getenv('HBNB_MYSQL_DB')),
                pool_pre_ping=True)

        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Query on the current database session (self.__session) all objects
        depending on the class name (argument cls)
        """
        if cls is None:
            objs = self.__session.query(State).all()
            objs.extend(self.__session.query(City).all())
            objs.extend(self.__session.query(User).all())
            objs.extend(self.__session.query(Place).all())
            objs.extend(self.__session.query(Review).all())
            objs.extend(self.__session.query(Amenity).all())
        else:
            if type(cls) is str:
                cls = eval(cls)
            objs = self.__session.query(cls)
        return {"{}.{}".format(type(o).__name__, o.id): o for o in objs}

    def new(self, obj):
        """
        Add the object to the current database session (self.__session)
        """
        self.__session.add(obj)

    def save(self):
        """
        Commit all changes of the current database session (self.__session)
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Delete from the current database session obj if not None
        """
        if obj:
            self.__session.delete(obj)

    def close(self):
        """Close the working SQLAlchemy session."""
        self.__session.close()

    def reload(self):
        """
        Create all tables in the database (feature of SQLAlchemy)
        """
        Base.metadata.create_all(self.__engine)
        se_fac = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(se_fac)
        self.__session = Session()
