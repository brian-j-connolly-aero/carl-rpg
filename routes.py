from flask import Blueprint, jsonify, Flask, render_template, request, redirect, url_for
# from flask_app import app, db
from models import Character, Party, Floor, Location, Item, History, db

bp = Blueprint('routes', __name__)
app = bp
# Character Routes


@app.route('/characters', methods=['GET', 'POST'])
def handle_characters():
    if request.method == 'GET':
        characters = Character.query.all()
        return jsonify([char.to_dict() for char in characters])
    elif request.method == 'POST':
        data = request.get_json()
        new_character = Character(**data)
        db.session.add(new_character)
        db.session.commit()
        return jsonify(new_character.to_dict()), 201


@app.route('/characters/<int:character_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_character(character_id):
    character = Character.query.get(character_id)
    if not character:
        return jsonify({'message': 'Character not found'}), 404

    if request.method == 'GET':
        return jsonify(character.to_dict())
    elif request.method == 'PUT':
        data = request.get_json()
        for key, value in data.items():
            setattr(character, key, value)
        db.session.commit()
        return jsonify(character.to_dict())
    elif request.method == 'DELETE':
        db.session.delete(character)
        db.session.commit()
        return '', 204

# Character List Route


@app.route('/character_list', methods=['GET', 'POST'])
def character_list():
    if request.method == 'POST':
        # Retrieve form data
        character_id = request.form.get('CharacterID')
        name = request.form['Name']
        char_class = request.form['Class']
        char_type = request.form['Type']
        level = request.form['Level']

        if character_id:
            # Update existing character
            character = Character.query.get(character_id)
            if character:
                character.Name = name
                character.Class = char_class
                character.Type = char_type
                character.Level = level
                db.session.commit()
        else:
            # Create new character
            new_character = Character(
                Name=name, Class=char_class, Type=char_type, Level=level)
            db.session.add(new_character)
            db.session.commit()

        return redirect(url_for('routes.character_list'))

    characters = Character.query.all()
    return render_template('characters.html', characters=characters)


@app.route('/new_character', methods=['GET'])
def new_character():
    if request.method == 'GET':
        return render_template('add_character.html')


@app.route('/add_character', methods=['GET', 'POST'])
def add_character():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form['name']
        hp = request.form['hp']
        mp = request.form['hp']
        char_class = request.form['class']
        level = request.form['level']
        role = request.form['role']
        description = request.form['description']
        new_character = Character(Name=name, HP=hp, HP_max=hp, MP=mp, MP_max=mp, Class=char_class,
                                  Level=level, PartyID=0, PartyRole=role, Description=description)
        db.session.add(new_character)
        db.session.commit()

        # Redirect to a new page or back to the character list, for instance
        return redirect(url_for('routes.character_list', character_id=0))
    return render_template('add_character.html')


@app.route('/characters/<int:character_id>/sheet', methods=['GET'])
def character_sheet(character_id):
    character = Character.query.get(character_id)
    if character:
        return render_template('character_sheet.html', character=character)
    else:
        return "Character not found", 404

# Party Routes


@app.route('/parties', methods=['GET', 'POST'])
def handle_parties():
    if request.method == 'GET':
        parties = Party.query.all()
        return jsonify([party.to_dict() for party in parties])
    elif request.method == 'POST':
        data = request.get_json()
        new_party = Party(**data)
        db.session.add(new_party)
        db.session.commit()
        return jsonify(new_party.to_dict()), 201


@app.route('/parties/<int:party_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_party(party_id):
    party = Party.query.get(party_id)
    if not party:
        return jsonify({'message': 'Party not found'}), 404

    if request.method == 'GET':
        return jsonify(party.to_dict())
    elif request.method == 'PUT':
        data = request.get_json()
        for key, value in data.items():
            setattr(party, key, value)
        db.session.commit()
        return jsonify(party.to_dict())
    elif request.method == 'DELETE':
        db.session.delete(party)
        db.session.commit()
        return '', 204

# Floor Routes


@app.route('/floors', methods=['GET', 'POST'])
def handle_floors():
    if request.method == 'GET':
        floors = Floor.query.all()
        return jsonify([floor.to_dict() for floor in floors])
    elif request.method == 'POST':
        data = request.get_json()
        new_floor = Floor(**data)
        db.session.add(new_floor)
        db.session.commit()
        return jsonify(new_floor.to_dict()), 201


@app.route('/floors/<int:floor_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_floor(floor_id):
    floor = Floor.query.get(floor_id)
    if not floor:
        return jsonify({'message': 'Floor not found'}), 404

    if request.method == 'GET':
        return jsonify(floor.to_dict())
    elif request.method == 'PUT':
        data = request.get_json()
        for key, value in data.items():
            setattr(floor, key, value)
        db.session.commit()
        return jsonify(floor.to_dict())
    elif request.method == 'DELETE':
        db.session.delete(floor)
        db.session.commit()
        return '', 204

# Location Routes


@app.route('/locations', methods=['GET', 'POST'])
def handle_locations():
    if request.method == 'GET':
        locations = Location.query.all()
        return jsonify([loc.to_dict() for loc in locations])
    elif request.method == 'POST':
        data = request.get_json()
        new_location = Location(**data)
        db.session.add(new_location)
        db.session.commit()
        return jsonify(new_location.to_dict()), 201


@app.route('/locations/<int:location_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_location(location_id):
    location = Location.query.get(location_id)
    if not location:
        return jsonify({'message': 'Location not found'}), 404

    if request.method == 'GET':
        return jsonify(location.to_dict())
    elif request.method == 'PUT':
        data = request.get_json()
        for key, value in data.items():
            setattr(location, key, value)
        db.session.commit()
        return jsonify(location.to_dict())
    elif request.method == 'DELETE':
        db.session.delete(location)
        db.session.commit()
        return '', 204

# Item Routes


@app.route('/items', methods=['GET', 'POST'])
def handle_items():
    if request.method == 'GET':
        items = Item.query.all()
        return jsonify([item.to_dict() for item in items])
    elif request.method == 'POST':
        data = request.get_json()
        new_item = Item(**data)
        db.session.add(new_item)
        db.session.commit()
        return jsonify(new_item.to_dict()), 201


@app.route('/items/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        return jsonify({'message': 'Item not found'}), 404

    if request.method == 'GET':
        return jsonify(item.to_dict())
    elif request.method == 'PUT':
        data = request.get_json()
        for key, value in data.items():
            setattr(item, key, value)
        db.session.commit()
        return jsonify(item.to_dict())
    elif request.method == 'DELETE':
        db.session.delete(item)
        db.session.commit()
        return '', 204


@app.route('/item_list', methods=['GET', 'POST'])
def item_list():
    if request.method == 'POST':
        # Retrieve form data
        item_id = request.form.get('ItemID')
        name = request.form['Name']
        item_type = request.form['Type']
        description = request.form['Description']
        equipped = request.form['Equipped']
        count = request.form['Count']

        if item_id:
            # Update existing item
            item = Item.query.get(item_id)
            if item:
                item.Name = name
                item.Type = item_type
                item.Description = description
                item.Equipped = equipped
                item.Count = count
                db.session.commit()
        else:
            # Create new item
            new_item = Item(Name=name, Type=item_type, Description=description, Equipped=equipped, Count=count)
            db.session.add(new_item)
            db.session.commit()

        return redirect(url_for('routes.item_list'))

    items = Item.query.all()
    return render_template('items.html', items=items)


@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form['name']
        item_type = request.form['type']
        description = request.form['description']
        equipped = request.form['equipped']
        count = request.form['count']
        character_id = request.form['character_id']
        location_id = request.form['location_id']

        new_item = Item(Name=name, Type=item_type, Description=description, Equipped=equipped, Count=count,
                        CharacterID=character_id, LocationID=location_id)
        db.session.add(new_item)
        db.session.commit()

        # Redirect to a new page or back to the item list, for instance
        return redirect(url_for('routes.item_list'))

    return render_template('add_item.html')


@app.route('/characters/<int:character_id>/item_list', methods=['GET'])
def character_item_list(character_id):
    character = Character.query.get(character_id)
    if character:
        items = character.items
        return render_template('character_items.html', character=character, items=items)
    else:
        return "Character not found", 404
# History Routes


@app.route('/history', methods=['GET', 'POST'])
def handle_history():
    if request.method == 'GET':
        history = History.query.all()
        return jsonify([hist.to_dict() for hist in history])
    elif request.method == 'POST':
        data = request.get_json()
        new_history = History(**data)
        db.session.add(new_history)
        db.session.commit()
        return jsonify(new_history.to_dict()), 201


@app.route('/history/<int:history_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_history_entry(history_id):
    history_entry = History.query.get(history_id)
    if not history_entry:
        return jsonify({'message': 'History entry not found'}), 404

    if request.method == 'GET':
        return jsonify(history_entry.to_dict())
    elif request.method == 'PUT':
        data = request.get_json()
        for key, value in data.items():
            setattr(history_entry, key, value)
        db.session.commit()
        return jsonify(history_entry.to_dict())
    elif request.method == 'DELETE':
        db.session.delete(history_entry)
        db.session.commit()
        return '', 204

# Extra Routes


@app.route('/characters/<int:character_id>/items')
def get_character_items(character_id):
    character = Character.query.get(character_id)
    if not character:
        return jsonify({'message': 'Character not found'}), 404
    items = character.items
    return jsonify([item.to_dict() for item in items])


@app.route('/locations/<int:location_id>/characters')
def get_location_characters(location_id):
    location = Location.query.get(location_id)
    if not location:
        return jsonify({'message': 'Location not found'}), 404
    characters = location.characters
    return jsonify([char.to_dict() for char in characters])
