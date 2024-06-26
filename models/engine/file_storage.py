#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls is None:
            return self.__objects
        if type(cls) == str:
            cls = eval(cls)
        filtered_objects = {k: v for k, v in self.__objects.items() if isinstance(v, cls)}
        return filtered_objects


    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.__objects[obj.__class__.__name__ + '.' + obj.id] = obj

    def save(self):
        """Saves storage dictionary to file"""
        json_objects = {k: v.to_dict() for k, v in self.__objects.items()}
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """Loads storage dictionary from file"""
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
    """deletes ///"""
    if obj is None:
        return
    key = obj.__class__.__name__ + '.' + obj.id
    if key in self.__objects:
        del self.__objects[key]