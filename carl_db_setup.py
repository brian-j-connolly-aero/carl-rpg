# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 13:25:34 2024

@author: cavsf
"""

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
import os
import time
import shutil

db_path = 'sqlite:///data/carl_database.db'
backup_path = 'data/old_tables'
Base = declarative_base()

# Define your models
class Party(Base):
    __tablename__ = 'Parties'
    
    PartyID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String, nullable=False)

class Floor(Base):
    __tablename__ = 'Floors'
    
    FloorID = Column(Integer, primary_key=True, autoincrement=True)
    FloorNumber = Column(Integer, nullable=False)
    Description = Column(Text, nullable=False)

class Location(Base):
    __tablename__ = 'Locations'
    
    LocationID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String, nullable=False)
    FloorID = Column(Integer, ForeignKey('Floors.FloorID'))
    Description = Column(Text)
    Attributes = Column(Text)
    
    floor = relationship("Floor")

class Character(Base):
    __tablename__ = 'Characters'
    
    CharacterID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String, nullable=False)
    Class = Column(String)
    Level = Column(Integer)
    PartyID = Column(Integer, ForeignKey('Parties.PartyID'))
    PartyRole = Column(String)
    LocationID = Column(Integer, ForeignKey('Locations.LocationID'))
    Attributes = Column(Text)
    
    party = relationship("Party")
    location = relationship("Location")

class Item(Base):
    __tablename__ = 'Items'
    
    ItemID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String, nullable=False)
    Type = Column(String)
    Description = Column(Text, nullable=False)
    Equipped = Column(String, nullable=False)
    Count = Column(Integer)
    CharacterID = Column(Integer, ForeignKey('Characters.CharacterID'))
    LocationID = Column(Integer, ForeignKey('Locations.LocationID'))
    Attributes = Column(Text)
    
    character = relationship("Character")
    location = relationship("Location")

class History(Base):
    __tablename__ = 'History'
    
    HistoryID = Column(Integer, primary_key=True, autoincrement=True)
    Description = Column(Text, nullable=False)


def create_tables(db_path):
    if os.path.exists(db_path.replace('sqlite:///', '')):
        if not os.path.exists(backup_path):
            os.makedirs(backup_path)
        shutil.copy(db_path.replace('sqlite:///', ''), os.path.join(backup_path, f'old_database-{time.strftime("%Y%m%d-%H%M%S")}.db'))
        os.remove(db_path.replace('sqlite:///', ''))
    else:
        print("The file does not exist")

    engine = create_engine(db_path)
    Base.metadata.create_all(engine)

# def get_history(db_path):
#     engine = create_engine(db_path)
#     Session = sessionmaker(bind=engine)
#     session = Session()
    
#     descriptions = session.query(History.Description).all()
#     all_descriptions = "".join([description[0] + "\n" for description in descriptions])
#     return all_descriptions



