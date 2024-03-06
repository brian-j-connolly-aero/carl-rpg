from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Define your models
class Party(db.Model):
    __tablename__ = 'Parties'
    
    PartyID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String, nullable=False)

class Floor(db.Model):
    __tablename__ = 'Floors'
    
    FloorID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FloorNumber = db.Column(db.Integer, nullable=False)
    Description = db.Column(db.Text, nullable=False)

class Location(db.Model):
    __tablename__ = 'Locations'
    
    LocationID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String, nullable=False)
    FloorID = db.Column(db.Integer, db.ForeignKey('Floors.FloorID'))
    Description = db.Column(db.Text)
    Attributes = db.Column(db.Text)
    
    floor = db.relationship("Floor")

class Character(db.Model):
    __tablename__ = 'Characters'
    
    CharacterID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String, nullable=False)
    HP = db.Column(db.Integer)
    HP_max = db.Column(db.Integer)
    MP = db.Column(db.Integer)
    MP_max = db.Column(db.Integer)
    Class = db.Column(db.String)
    Type = db.Column(db.String)
    Level = db.Column(db.Integer)
    PartyID = db.Column(db.Integer, db.ForeignKey('Parties.PartyID'))
    PartyRole = db.Column(db.String)
    LocationID = db.Column(db.Integer, db.ForeignKey('Locations.LocationID'))
    Description= db.Column(db.String)
    Attributes = db.Column(db.Text)
    
    party = db.relationship("Party")
    location = db.relationship("Location")

class Item(db.Model):
    __tablename__ = 'Items'
    
    ItemID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String, nullable=False)
    Type = db.Column(db.String)
    Description = db.Column(db.Text, nullable=False)
    Equipped = db.Column(db.String, nullable=False)
    Count = db.Column(db.Integer)
    CharacterID = db.Column(db.Integer, db.ForeignKey('Characters.CharacterID'))
    LocationID = db.Column(db.Integer, db.ForeignKey('Locations.LocationID'))
    Attributes = db.Column(db.Text)
    
    character = db.relationship("Character")
    location = db.relationship("Location")

class History(db.Model):
    __tablename__ = 'History'
    
    HistoryID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Description = db.Column(db.Text, nullable=False)