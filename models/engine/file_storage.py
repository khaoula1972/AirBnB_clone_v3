#!/usr/bin/python3
"""
This file contains class
"""
import json


class FileStorage:
    """
    class that serializes instances to a JSON file and
    deserializes JSON file to instances
    """
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """
        Returns the dictionary of all objects.
        """
        if cls is not None:
            if type(cls) is str:
                cls = eval(cls)
            cls_dict = {}
            for k, v in self.__objects.items():
                if type(v) is cls:
                    cls_dict[k] = v
            return cls_dict
        return self.__objects

    def new(self, obj):
        """
        Sets in obejts the obj with key
        """
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """
        Serializes __objects to the JSON file.
        """
        serialized_objects = {}
        for key, value in FileStorage.__objects.items():
            serialized_objects[key] = value.to_dict()

        with open(FileStorage.__file_path, 'w') as file:
            json.dump(serialized_objects, file)

    def reload(self):
        """
        Deserializes the JSON file to __objects.
        """
        # Let's import first
        # if imported outside, this will cause circular import
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        classes = {
                'BaseModel': BaseModel, 'User': User,
                "State": State, "City": City, "Review": Review,
                "Amenity": Amenity, "Place": Place
                }

        try:
            data = {}

            with open(FileStorage.__file_path, 'r') as file:
                data = json.load(file)
                for key, val in data.items():
                    self.all()[key] = classes[val['__class__']](**val)

        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes obj from __objects if it's inside"""
        if obj is not None:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            if key in FileStorage.__objects:
                del FileStorage.__objects[key]

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls not in classes.values():
            return None

        all_cls = models.storage.all(cls)
        for value in all_cls.values():
            if (value.id == id):
                return value

        return None

    def count(self, cls=None):
        """
        count the number of objects in storage. If cls is provided,
        count objects of that class; otherwise, count all objects
        """
        all_class = classes.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(models.storage.all(clas).values())
        else:
            count = len(models.storage.all(cls).values())

        return count

    """
    def get(self, cls, id):
        Retrieve one object by class and ID
        if cls and id:
            key = "{}.{}".format(cls.__name__, id)
            return self.all(cls).get(key, None)
        return None

    def count(self, cls=None):
    
        count the number of objects in storage. If cls is provided,
        count objects of that class; otherwise, count all objects
        
        if cls:
            return len(self.all(cls))
        else:
            count = 0
            for cnt in [State, City, User, Place, Review, Amenity]:
                count += len(self.all(cnt))
            return count"""
