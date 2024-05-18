# -*- coding: utf-8 -*-
"""
Created on Fri May 17 17:36:44 2024

@author: cavsf
"""

from models import Character, Party, Floor, Location, Item, History, db
from config import db_path, backup_path
import shutil
import os
import time
from sqlalchemy.inspection import inspect

# General Services
def get_by_id(model,id):
    return model.query.get(id)

def update(instance, updated_data):
    for key, value in updated_data.items():
        setattr(instance, key, value)
    db.session.commit()
    return instance

def get_all(model):
    return model.query.all()

def drop_database():
    shutil.copy(db_path.replace('sqlite:///', ''), os.path.join(backup_path, f'old_database-{time.strftime("%Y%m%d-%H%M%S")}.db'))
    os.remove(db_path.replace('sqlite:///', ''))
    return

def get_columns(model):
    return inspect(model).columns.keys()

def get_current_values(instance):
    # Get column attributes
    attributes = {column.key: getattr(instance, column.key) for column in inspect(instance).mapper.column_attrs}

    # Get first-level related attributes
    for relationship in inspect(instance).mapper.relationships:
        related_value = getattr(instance, relationship.key)
        if relationship.uselist:
            attributes[relationship.key] = [
                {column.key: getattr(item, column.key) for column in inspect(item).mapper.column_attrs} for item in related_value
            ]
        else:
            attributes[relationship.key] = (
                {column.key: getattr(related_value, column.key) for column in inspect(related_value).mapper.column_attrs}
                if related_value else None
            )
    return attributes

# Character Services
def get_all_characters():
    return Character.query.all()

def get_character_by_id(character_id):
    return Character.query.get(character_id)

def create_character(data):
    new_character = Character(**data)
    db.session.add(new_character)
    db.session.commit()
    return new_character

def update_character(character, data):
    for key, value in data.items():
        setattr(character, key, value)
    db.session.commit()
    return character

def delete_character(character):
    db.session.delete(character)
    db.session.commit()
    
# def get_character_items(character):
    

# Party Services
def get_all_parties():
    return Party.query.all()

def get_party_by_id(party_id):
    return Party.query.get(party_id)

def create_party(data):
    new_party = Party(**data)
    db.session.add(new_party)
    db.session.commit()
    return new_party

def update_party(party, data):
    for key, value in data.items():
        setattr(party, key, value)
    db.session.commit()
    return party

def delete_party(party):
    db.session.delete(party)
    db.session.commit()

# Floor Services
def get_all_floors():
    return Floor.query.all()

def get_floor_by_id(floor_id):
    return Floor.query.get(floor_id)

def create_floor(data):
    new_floor = Floor(**data)
    db.session.add(new_floor)
    db.session.commit()
    return new_floor

def update_floor(floor, data):
    for key, value in data.items():
        setattr(floor, key, value)
    db.session.commit()
    return floor

def delete_floor(floor):
    db.session.delete(floor)
    db.session.commit()

# Location Services
def get_all_locations():
    return Location.query.all()

def get_location_by_id(location_id):
    return Location.query.get(location_id)

def create_location(data):
    new_location = Location(**data)
    db.session.add(new_location)
    db.session.commit()
    return new_location

def update_location(location, data):
    for key, value in data.items():
        setattr(location, key, value)
    db.session.commit()
    return location

def delete_location(location):
    db.session.delete(location)
    db.session.commit()

# Item Services
def get_all_items():
    return Item.query.all()

def get_item_by_id(item_id):
    return Item.query.get(item_id)

def create_item(data):
    new_item = Item(**data)
    db.session.add(new_item)
    db.session.commit()
    return new_item

def update_item(item, data):
    for key, value in data.items():
        setattr(item, key, value)
    db.session.commit()
    return item

def delete_item(item):
    db.session.delete(item)
    db.session.commit()

# History Services
def get_all_history():
    return History.query.all()

def get_history_by_id(history_id):
    return History.query.get(history_id)

def create_history(data):
    new_history = History(**data)
    db.session.add(new_history)
    db.session.commit()
    return new_history

def update_history(history_entry, data):
    for key, value in data.items():
        setattr(history_entry, key, value)
    db.session.commit()
    return history_entry

def delete_history(history_entry):
    db.session.delete(history_entry)
    db.session.commit()

# # Spell Services
# def get_all_spells():
#     return Spell.query.all()

# def get_spell_by_id(spell_id):
#     return Spell.query.get(spell_id)

# def create_spell(data):
#     new_spell = Spell(**data)
#     db.session.add(new_spell)
#     db.session.commit()
#     return new_spell

# def update_spell(spell, data):
#     for key, value in data.items():
#         setattr(spell, key, value)
#     db.session.commit()
#     return spell

# def delete_spell(spell):
#     db.session.delete(spell)
#     db.session.commit()
