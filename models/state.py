#!/usr/bin/python3
""" State module for the HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String


class State(BaseModel, Base):
    """ State class to store state information """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    if models.storage_type == "db":
        cities = relationship("City", backref="state",
                              cascade="all, delete")
    else:
        @property
        def cities(self):
            """Getter attribute that returns the list of City instances
            with state_id equals to the current State.id"""
            from models import storage
            cities = storage.all("City").values()
            return [city for city in cities if city.state_id == self.id]
