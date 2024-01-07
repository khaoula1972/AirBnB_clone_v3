#!/usr/bin/python3
"""
This conatins the class amenity
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Table, ForeignKey
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """
    This is Amenity class that inherets from BaseModel
    """

    __tablename__ = 'amenities'

    name = Column(String(128), nullable=False)

    place_amenities = relationship("Place",
                                   secondary='place_amenity',
                                   back_populates="amenities", viewonly=False)
