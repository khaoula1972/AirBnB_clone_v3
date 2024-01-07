#!/usr/bin/python3
"""
This conatins a class calle Basemodel
"""
import uuid
import models
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import DateTime
from datetime import datetime
from sqlalchemy import Column, String

Base = declarative_base()


class BaseModel:
    """
    This is a class that defines all common attributes/methods
    for other classes.
    """
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """
        Initialization...
        """

        if kwargs:
            for key, value in kwargs.items():
                if key == '__class__':
                    continue  # To skip the class attribute
                elif key == 'created_at' or key == 'updated_at':
                    setattr(
                            self, key,
                            datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                            )
                else:
                    setattr(self, key, value)
            if 'id' not in kwargs:
                # To generate a unique ID
                self.id = str(uuid.uuid4())
            if 'created_at' not in kwargs:
                # To set creation timestamp
                self.created_at = datetime.now()
            if 'updated_at' not in kwargs:
                self.updated_at = datetime.now()  # Initial update
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

    def save(self):
        """
        updates the public instance attribute updated_at
        with the current datetime
        """
        models.storage.new(self)
        models.storage.save()

    def __str__(self):
        """
        To print
        """

        obj_dict = self.__dict__.copy()
        obj_dict.pop("_sa_instance_state", None)
        return "[{}] ({}) {}".format(
                type(self).__name__, self.id, obj_dict
                )

    def to_dict(self):
        """
        returns a dictionary containing all keys/values of __dict__
        """

        class_name = self.__class__.__name__
        obj_dict = self.__dict__.copy()
        obj_dict["__class__"] = class_name
        obj_dict["created_at"] = self.created_at.isoformat()
        obj_dict["updated_at"] = self.updated_at.isoformat()
        obj_dict.pop("_sa_instance_state", None)
        return obj_dict

    def delete(self):
        """delete instance"""
        models.storage.delete(self)
