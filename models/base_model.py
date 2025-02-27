#!/usr/bin/python3
"""This module defines a base class for all models in the hbnb clone"""
import uuid
from datetime import datetime

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, DateTime

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), primary_key=True, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow(), nullable=False)

    def __init__(self, *args, **kwargs):
        """Instantiates a new model"""
        if not kwargs:
            from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

        else:
            try:
                kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
                kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
                del kwargs['__class__']
                self.__dict__.update(kwargs)
                for k, v in kwargs.items():
                    setattr(self, k, v)
            except KeyError:
                 self.id = str(uuid.uuid4())
                 self.created_at = datetime.now()
                 self.updated_at = datetime.now()
                 for k, v in kwargs.items():
                     setattr(self, k, v)
        # else:
        #     kwargs.pop('__class__')
        #     for k, v in kwargs.items():
        #         if k == 'created_at' or k == 'updated_at':
        #             v = datetime.strptime(k,
        #                                   '%Y-%m-%dT%H:%M:%S.%f')
        #             self.__dict__.update(kwargs)
        #         setattr(self, k, v)

    def __str__(self):
        """Returns a string representation of the instance"""
        if '_sa_instance_state' in self.__dict__:
            self.__dict__.pop('_sa_instance_state')
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}

        #if '_sa_instance_state' in self.__dict__:
        #    self.__dict__.pop('_sa_instance_state')

        dictionary.update(self.__dict__)
        dictionary.update(
            {'__class__': (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()

        return dictionary

    def delete(self):
        from models import storage
        storage.delete(self)
