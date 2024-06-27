#!/usr/bin/python3
"""File storage module to manage data files"""
import json
from importlib import import_module

models_dict = {
    "BaseModel": "base_model",
    "User": "user",
    "Amenity": "amenity",
    "City": "city",
    "Place": "place",
    "Review": "review",
    "State": "state"
    }


class FileStorage:
    """
    Serializes instances to json file
    and deserializes json to file
    """

    __file_path = "file.json"
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
        """
        Sets in __objects the obj with
        key <obj class name>.id
        """
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Serializes __objects to the json file with __file_path"""
        # converting the objects in __objects into dictionaries
        obj_dict = {}
        for key, value in self.__objects.items():
            obj_dict[key] = value.to_dict()

        # turn them to json string then save
        with open(self.__file_path, "w") as f:
            json_str = json.dumps(obj_dict)
            f.write(json_str)

    def reload(self):
        """Deserializes JSON to __objects if the file exists"""

        try:
            # if the file exists: file -> json string -> object dict -> objects
            with open(self.__file_path, "r") as f:
                obj_dict = json.load(f)
                for key, obj in obj_dict.items():
                    class_name = obj["__class__"]
                    module_path = "models.{}".format(models_dict[class_name])
                    module = import_module(module_path)
                    cls = getattr(module, class_name)
                    self.__objects[key] = cls(**obj)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes object"""
        if obj is None:
            return
        key = obj.__class__.__name__ + '.' + obj.id
        if key in self.__objects:
            del self.__objects[key]
