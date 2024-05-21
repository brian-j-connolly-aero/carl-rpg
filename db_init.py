from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, Party, Floor, Location, Character, Item, History
import config
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.Config.SQLALCHEMY_DATABASE_URI
db.init_app(app)


def create_db():
    with app.app_context():
        db.create_all()



        party = Party(Name="No Party")
        db.session.add(party)

        # Create fake floors
        with open (r"C:\Users\cavsf\Desktop\carl\data\floors.json") as f:
            floors_dict=json.load(f)
            for index,(name,floor_dict) in enumerate(floors_dict.items()):
                floor_number=index+1
                floor = Floor(Name=name, FloorNumber=floor_number, Description=floor_dict['Description'])
                db.session.add(floor)
                for loc in floor_dict['Locations']:
                    location=Location(Name=loc['Name'],FloorID=floor.ID,Description=loc['Description'])
                    db.session.add(location)
        db.session.commit()



        # # Create fake characters
        # parties = Party.query.all()
        # locations = Location.query.all()
        # for _ in range(50):
        #     character = Character(
        #         Name=fake.name(),
        #         HP=fake.random_int(min=50, max=100),
        #         HP_max=fake.random_int(min=50, max=100),
        #         MP=fake.random_int(min=20, max=50),
        #         MP_max=fake.random_int(min=20, max=50),
        #         Class=fake.job(),
        #         Type=fake.word(),
        #         Level=fake.random_int(min=1, max=20),
        #         PartyID=fake.random_element(
        #             elements=[party.ID for party in parties]),
        #         PartyRole=fake.job(),
        #         LocationID=fake.random_element(
        #             elements=[location.ID for location in locations]),
        #         Description=fake.text(),
        #         Attributes="None"
        #     )
        #     db.session.add(character)

        # db.session.commit()

        # # Create fake items
        # characters = Character.query.all()
        # for _ in range(100):
        #     item = Item(
        #         Name=fake.word(),
        #         Type=fake.word(),
        #         Description=fake.text(),
        #         # Equipped=str(fake.boolean()),
        #         Count=fake.random_int(min=1, max=10),
        #         CharacterID=fake.random_element(
        #             elements=[character.ID for character in characters]),
        #         LocationID=fake.random_element(
        #             elements=[location.ID for location in locations]),
        #         Attributes="None"
        #     )
        #     db.session.add(item)

        # db.session.commit()

        # Create history
        with open('data/preprompt.txt','r') as f:
            history = History(Description=f.read(),Name="Background")
            db.session.add(history)

        db.session.commit()


        print('Initial data added to the database.')


if __name__ == '__main__':
    create_db()
