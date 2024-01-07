#!/usr/bin/python3
"""
This conatins the class state
"""
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """
    This is State class that inherets from BaseModel
    """

    __tablename__ = 'states'

    name = Column(String(128), nullable=False)

    cities = relationship(
            "City", backref="state", cascade="all, delete-orphan"
            )

    if os.getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            """getter attribute for cities"""
            from models import storage
            from models.city import City

            city_list = []
            for city_id, city in storage.all(City).items():
                if city.state_id == self.id:
                    city_list.append(city)
            return (city_list)
