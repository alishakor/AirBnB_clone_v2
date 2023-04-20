#!/usr/bin/python3
"""This module defines a class Place"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.amenity import Amenity


if models.storage_type == 'db':
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id'), primary_key=True,
                                 nullable=False),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id'),
                                 primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """This class defines a place by various attributes"""

    __tablename__ = 'places'

    if models.storage_type == 'db':
        amenities = relationship('Amenity', secondary=place_amenity,
                                 backref='places', viewonly=False)
    else:
        @property
        def reviews(self):
            """Getter attribute that returns the list of Review instances
               with place_id equals to the current Place.id"""
            review_list = []
            all_reviews = models.storage.all('Review')
            for review in all_reviews.values():
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list

        @property
        def amenities(self):
            """Getter attribute that returns the list of Amenity instances
               based on the attribute amenity_ids that contains all Amenity.id
               linked to the Place"""
            amenity_list = []
            all_amenities = models.storage.all('Amenity')
            for amenity in all_amenities.values():
                if amenity.id in self.amenity_ids:
                    amenity_list.append(amenity)
            return amenity_list

        @amenities.setter
        def amenities(self, amenity):
            """Setter attribute that handles append method
               for adding an Amenity.id to the attribute
               amenity_ids. This method should accept only Amenity object,
               otherwise, do nothing."""
            if isinstance(amenity, Amenity):
                if amenity.id not in self.amenity_ids:
                    self.amenity_ids.append(amenity.id)
            else:
                pass

    # Rest of the Place class definition...
