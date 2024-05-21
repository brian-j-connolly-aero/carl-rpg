from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from faker import Faker
from models import db, Party, Floor, Location, Character, Item, History
import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.Config.SQLALCHEMY_DATABASE_URI
db.init_app(app)

fake = Faker()


def create_fake_data():
    with app.app_context():
        db.create_all()

        # Create fake parties
        for _ in range(10):
            party = Party(Name=fake.company())
            db.session.add(party)

        # Create fake floors
        for _ in range(5):
            floor = Floor(Name=fake.country(), FloorNumber=fake.random_int(
                min=1, max=10), Description=fake.text())
            db.session.add(floor)

        db.session.commit()

        # Create fake locations
        floors = Floor.query.all()
        for _ in range(20):
            location = Location(Name=fake.street_name(), FloorID=fake.random_element(
                elements=[floor.ID for floor in floors]), Description=fake.text())
            db.session.add(location)

        db.session.commit()

        # Create fake characters
        parties = Party.query.all()
        locations = Location.query.all()
        for _ in range(50):
            character = Character(
                Name=fake.name(),
                HP=fake.random_int(min=50, max=100),
                HP_max=fake.random_int(min=50, max=100),
                MP=fake.random_int(min=20, max=50),
                MP_max=fake.random_int(min=20, max=50),
                Class=fake.job(),
                Type=fake.word(),
                Level=fake.random_int(min=1, max=20),
                PartyID=fake.random_element(
                    elements=[party.ID for party in parties]),
                PartyRole=fake.job(),
                LocationID=fake.random_element(
                    elements=[location.ID for location in locations]),
                Description=fake.text(),
                Attributes="None"
            )
            db.session.add(character)

        db.session.commit()

        # Create fake items
        characters = Character.query.all()
        for _ in range(100):
            item = Item(
                Name=fake.word(),
                Type=fake.word(),
                Description=fake.text(),
                # Equipped=str(fake.boolean()),
                Count=fake.random_int(min=1, max=10),
                CharacterID=fake.random_element(
                    elements=[character.ID for character in characters]),
                LocationID=fake.random_element(
                    elements=[location.ID for location in locations]),
                Attributes="None"
            )
            db.session.add(item)

        db.session.commit()

        # Create fake history entries
        for _ in range(30):
            history = History(Description=fake.text())
            db.session.add(history)

        db.session.commit()


        print('Fake data added to the database.')


if __name__ == '__main__':
    create_fake_data()
