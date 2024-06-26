#!/usr/bin/python3
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

class FileStorage:

    __file_path = 'fiii.json'
    __objects = {}

    def all(self, cls=None):
        if cls is None:
            return self.__objects
        if type(cls) == str:
            cls = eval(cls)
        filtered_objects = {k: v for k, v in self.__objects.items() if isinstance(v, cls)}
        return filtered_objects

    def new(self, obj):
        self.__objects[obj.__class__.__name__ + '.' + obj.id] = obj

    def save(self):
        json_objects = {k: v.to_dict() for k, v in self.__objects.items()}
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        try:
            with open(self.__file_path, 'r') as f:
                json_objects = json.load(f)
                for k, v in json_objects.items():
                    cls_name = v['__class__']
                    cls = eval(cls_name)
                    self.__objects[k] = cls(**v)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        if obj is None:
            return
        key = obj.__class__.__name__ + '.' + obj.id
        if key in self.__objects:
            del self.__objects[key]