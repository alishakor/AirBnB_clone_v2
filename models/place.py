#!/usr/bin/python3
"""This module defines a class Place"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.amenity import Amenity
from os import getenv
import models


place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id',
                              String(60),
                              ForeignKey('places.id'),
                              primary_key=True,
                              nullable=False),
                      Column('amenity_id',
                             String(60),
                             ForeignKey('amenities.id'),
                             primary_key=True,
                             nullable=False))


class Place(BaseModel, Base):
    """This class defines a place by various attributes"""
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []
    if getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship("Review", backref="place",
                               cascade="all, delete")
    elif getenv("HBNB_TYPE_STORAGE") == "file":
        @property
        def reviews(self):
            review_list = []
            for key, value in models.storage.all().items:
                if value.place_id == value.place.id:
                    review_list.append(value)
            return review_list
    if getenv("HBNB_TYPE_STORAGE") == "db":
        amenities = relationship("Amenity",
                                 secondary=place_amenity,
                                 viewonly=False)
    elif getenv("HBNB_TYPE_STORAGE") == "file":
        @property
        def amenities(self):
            """
            returns the list of Amenity instances based on
            the attribute amenity_ids that contains all
            Amenity.id linked to the Place
            """

            amenity_val = models.storage.all(Amenity).values()
            amenities_list = []
            for amenity in amenity_val:
                if amenity.place_id == self.id:
                    ammenities_list.append(amenity)
            return amenities_list

        @ammenities.setter
        def amenities(self, obj):
            """handles append method for adding an
            Amenity.id to the attribute amenity_ids.
            This method should accept only Amenity object,
            otherwise, do nothing.
            """
            if not isinstance(obj, Amenity):
                return
            self.amenity_ids.append(obj.id)

