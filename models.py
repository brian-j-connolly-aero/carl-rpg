from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Define your models


class Party(db.Model):
    __tablename__ = 'Parties'

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String, nullable=False)


class Floor(db.Model):
    __tablename__ = 'Floors'

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String, nullable=False)
    FloorNumber = db.Column(db.Integer, nullable=False)
    Description = db.Column(db.Text, nullable=False)


class Location(db.Model):
    __tablename__ = 'Locations'

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String, nullable=False)
    FloorID = db.Column(db.Integer, db.ForeignKey('Floors.ID'))
    Description = db.Column(db.Text)
    Attributes = db.Column(db.Text)

    floor = db.relationship("Floor")


class Character(db.Model):
    __tablename__ = 'Characters'

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String, nullable=False, unique=True)
    HP = db.Column(db.Integer)
    HP_max = db.Column(db.Integer)
    MP = db.Column(db.Integer)
    MP_max = db.Column(db.Integer)
    Class = db.Column(db.String)
    Type = db.Column(db.String)
    Level = db.Column(db.Integer)
    PartyID = db.Column(db.Integer, db.ForeignKey('Parties.ID'))
    PartyRole = db.Column(db.String)
    LocationID = db.Column(db.Integer, db.ForeignKey('Locations.ID'))
    Description = db.Column(db.String)
    Attributes = db.Column(db.Text)

    party = db.relationship("Party", backref="character")
    location = db.relationship("Location", backref="character")
    items = db.relationship("Item", backref="character")


class Item(db.Model):
    __tablename__ = 'Items'

    ItemID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String, nullable=False)
    Type = db.Column(db.String)
    Description = db.Column(db.Text, nullable=False)
    #Equipped = db.Column(db.String, nullable=False)
    Count = db.Column(db.Integer)
    CharacterID = db.Column(
        db.Integer, db.ForeignKey('Characters.ID'))
    LocationID = db.Column(db.Integer, db.ForeignKey('Locations.ID'))
    Attributes = db.Column(db.Text)

    location = db.relationship("Location")


class History(db.Model):
    __tablename__ = 'History'

    HistoryID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Description = db.Column(db.Text, nullable=False)
