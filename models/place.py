#!/usr/bin/python3
"""
This conatins the class place
"""
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.review import Review
from sqlalchemy.orm import relationship
from os import getenv
from sqlalchemy import Column, Table, String, Integer, Float, ForeignKey

# Define the association table

association_table = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id'), nullable=False,
                                 primary_key=True),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id'), nullable=False,
                                 primary_key=True)
                          )


class Place(BaseModel, Base):
    """
    This is Place class that inherets from BaseModel
    """

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

    reviews = relationship("Review", cascade="delete", backref="place")
    amenities = relationship("Amenity",
                             secondary=association_table,
                             back_populates="place_amenities", viewonly=False)

    if getenv("HBNB_TYPE_STORAGE", None) != "db":
        @property
        def reviews(self):
            """Getter attribute that returns the list of Review instances"""

            from models import storage
            reviews_list = []
            for review in storage.all(Review).values():
                if review.place_id == self.id:
                    reviews_list.append(review)
            return reviews_list

        @property
        def amenities(self):
            """Getter attribute for amenities in FileStorage"""
            return [model.amenities.get(amenity_id) for amenity_id in
                    self.amenity_ids]

        @amenities.setter
        def amenities(self, ameni_ty):
            """Setter attribute for amenities in FileStorage"""
            if isinstance(ameni_ty, Amenity):
                self.amenity_ids.append(ameni_ty.id)
