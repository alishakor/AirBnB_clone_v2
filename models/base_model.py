#!/usr/bin/python3
""" Base model for the HBNB project """
import uuid
from datetime import datetime
import models
from sqlalchemy import Column, String, DateTime

Base = models.Base


class BaseModel:
    """ Base class for other classes to inherit from """
    id = Column(String(60), unique=True, nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """ Constructor method """
        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    setattr(self, key, value)
            if 'id' not in kwargs:
                self.id = str(uuid.uuid4())
            time = datetime.utcnow()
            if 'created_at' not in kwargs:
                self.created_at = time
            if 'updated_at' not in kwargs:
                self.updated_at = time
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.utcnow()
            models.storage.new(self)

    def __str__(self):
        """ String representation of the BaseModel instance """
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id,
                                     self.__dict__)

    def save(self):
        """ Save the BaseModel instance """
        self.updated_at = datetime.utcnow()
        models.storage.save()

    def to_dict(self):
        """ Return a dictionary containing all keys/values of __dict__ """
        dictionary = dict(self.__dict__)
        dictionary['__class__'] = self.__class__.__name__
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        if '_sa_instance_state' in dictionary:
            del dictionary['_sa_instance_state']
        return dictionary

    def delete(self):
        """ Delete the current instance from the storage """
        models.storage.delete(self)
