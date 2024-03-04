# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 16:05:48 2024

@author: cavsf
"""
#need to handle db reset properly
# Create routing to display page with character as plain text
# Add item/ItemID routing
# Define separate function outside of route with **kwargs to return formatted character update


from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os

app = Flask(__name__, template_folder='html')
base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, 'data', 'carl_database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SECRET_KEY'] = 'AAAAAAAAAAA'

db = SQLAlchemy(app)

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
    Class = db.Column(db.String)
    Type = db.Column(db.String)
    Level = db.Column(db.Integer)
    PartyID = db.Column(db.Integer, db.ForeignKey('Parties.PartyID'))
    PartyRole = db.Column(db.String)
    LocationID = db.Column(db.Integer, db.ForeignKey('Locations.LocationID'))
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


# Flask-Admin setup
admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')
admin.add_view(ModelView(Party, db.session))
admin.add_view(ModelView(Floor, db.session))
admin.add_view(ModelView(Location, db.session))
admin.add_view(ModelView(Character, db.session))
admin.add_view(ModelView(Item, db.session))
admin.add_view(ModelView(History, db.session))
@app.route('/characters', methods=['GET','POST'])
def characters():
    if request.method=='GET':
        character_list = Character.query.all()
        return render_template('characters.html', character=character_list)
        # character_details = []
        # for character in character_list:
        #     character_details.append(f"ID: {character.CharacterID}, Name: {character.Name}, Class: {character.Class}, Type: {character.Type}, Level: {character.Level}")
        # return "\n".join(character_details)
    if request.method=='POST':
        data = request.get_json()
        character_id = data.get('CharacterID')
        if not character_id:
            return jsonify({'message': 'CharacterID is required'}), 400
    
        character = Character.query.get(character_id)
        if not character:
            return jsonify({'message': 'Character not found'}), 404
    
        # Iterate over each key in the JSON data
        for key in data:
            if key == 'CharacterID':
                continue  # Skip the CharacterID field, it's not to be updated
            if hasattr(character, key):
                # Update the attribute if the Character model has this attribute
                setattr(character, key, data[key])
    
        db.session.commit()
        return jsonify({'message': 'Character updated successfully'}), 200  

if __name__ == '__main__':
    with app.app_context():
        # Create database tables
        db.create_all()
    app.run(debug=True)


