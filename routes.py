from flask import Blueprint, jsonify, request, render_template, redirect, url_for
import services

bp = Blueprint('routes', __name__)

# Character Routes
@bp.route('/characters', methods=['GET', 'POST'])
def handle_characters():
    if request.method == 'GET':
        characters = services.get_all_characters()
        return jsonify([char.to_dict() for char in characters])
    elif request.method == 'POST':
        data = request.get_json()
        new_character = services.create_character(data)
        return jsonify(new_character.to_dict()), 201

@bp.route('/characters/<int:character_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_character(character_id):
    character = services.get_character_by_id(character_id)
    if not character:
        return jsonify({'message': 'Character not found'}), 404

    if request.method == 'GET':
        return jsonify(character.to_dict())
    elif request.method == 'PUT':
        data = request.get_json()
        updated_character = services.update_character(character, data)
        return jsonify(updated_character.to_dict())
    elif request.method == 'DELETE':
        services.delete_character(character)
        return '', 204

# Character List Route
@bp.route('/character_list', methods=['GET', 'POST'])
def character_list():
    if request.method == 'POST':
        character_id = request.form.get('CharacterID')
        name = request.form['Name']
        char_class = request.form['Class']
        char_type = request.form['Type']
        level = request.form['Level']

        if character_id:
            character = services.get_character_by_id(character_id)
            if character:
                data = {
                    'Name': name,
                    'Class': char_class,
                    'Type': char_type,
                    'Level': level
                }
                services.update_character(character, data)
        else:
            data = {
                'Name': name,
                'Class': char_class,
                'Type': char_type,
                'Level': level
            }
            services.create_character(data)

        return redirect(url_for('routes.character_list'))

    characters = services.get_all_characters()
    return render_template('characters.html', characters=characters)

@bp.route('/new_character', methods=['GET'])
def new_character():
    if request.method == 'GET':
        return render_template('add_character.html')

@bp.route('/add_character', methods=['GET', 'POST'])
def add_character():
    if request.method == 'POST':
        name = request.form['name']
        hp = request.form['hp']
        mp = request.form['mp']
        char_class = request.form['class']
        level = request.form['level']
        role = request.form['role']
        description = request.form['description']
        data = {
            'Name': name,
            'HP': hp,
            'HP_max': hp,
            'MP': mp,
            'MP_max': mp,
            'Class': char_class,
            'Level': level,
            'PartyID': 0,
            'PartyRole': role,
            'Description': description
        }
        new_character = services.create_character(data)
        return redirect(url_for('routes.character_list', character_id=new_character.CharacterID))
    return render_template('add_character.html')

@bp.route('/characters/<int:character_id>/sheet', methods=['GET'])
def character_sheet(character_id):
    character = services.get_character_by_id(character_id)
    if character:
        return render_template('character_sheet.html', character=character)
    else:
        return "Character not found", 404

# Party Routes
@bp.route('/parties', methods=['GET', 'POST'])
def handle_parties():
    if request.method == 'GET':
        parties = services.get_all_parties()
        return jsonify([party.to_dict() for party in parties])
    elif request.method == 'POST':
        data = request.get_json()
        new_party = services.create_party(data)
        return jsonify(new_party.to_dict()), 201

@bp.route('/parties/<int:party_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_party(party_id):
    party = services.get_party_by_id(party_id)
    if not party:
        return jsonify({'message': 'Party not found'}), 404

    if request.method == 'GET':
        return jsonify(party.to_dict())
    elif request.method == 'PUT':
        data = request.get_json()
        updated_party = services.update_party(party, data)
        return jsonify(updated_party.to_dict())
    elif request.method == 'DELETE':
        services.delete_party(party)
        return '', 204

# Floor Routes
@bp.route('/floors', methods=['GET', 'POST'])
def handle_floors():
    if request.method == 'GET':
        floors = services.get_all_floors()
        return jsonify([floor.to_dict() for floor in floors])
    elif request.method == 'POST':
        data = request.get_json()
        new_floor = services.create_floor(data)
        return jsonify(new_floor.to_dict()), 201

@bp.route('/floors/<int:floor_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_floor(floor_id):
    floor = services.get_floor_by_id(floor_id)
    if not floor:
        return jsonify({'message': 'Floor not found'}), 404

    if request.method == 'GET':
        return jsonify(floor.to_dict())
    elif request.method == 'PUT':
        data = request.get_json()
        updated_floor = services.update_floor(floor, data)
        return jsonify(updated_floor.to_dict())
    elif request.method == 'DELETE':
        services.delete_floor(floor)
        return '', 204

# Location Routes
@bp.route('/locations', methods=['GET', 'POST'])
def handle_locations():
    if request.method == 'GET':
        locations = services.get_all_locations()
        return jsonify([loc.to_dict() for loc in locations])
    elif request.method == 'POST':
        data = request.get_json()
        new_location = services.create_location(data)
        return jsonify(new_location.to_dict()), 201

@bp.route('/locations/<int:location_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_location(location_id):
    location = services.get_location_by_id(location_id)
    if not location:
        return jsonify({'message': 'Location not found'}), 404

    if request.method == 'GET':
        return jsonify(location.to_dict())
    elif request.method == 'PUT':
        data = request.get_json()
        updated_location = services.update_location(location, data)
        return jsonify(updated_location.to_dict())
    elif request.method == 'DELETE':
        services.delete_location(location)
        return '', 204

# Item Routes
@bp.route('/items', methods=['GET', 'POST'])
def handle_items():
    if request.method == 'GET':
        items = services.get_all_items()
        return jsonify([item.to_dict() for item in items])
    elif request.method == 'POST':
        data = request.get_json()
        new_item = services.create_item(data)
        return jsonify(new_item.to_dict()), 201

@bp.route('/items/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_item(item_id):
    item = services.get_item_by_id(item_id)
    if not item:
        return jsonify({'message': 'Item not found'}), 404

    if request.method == 'GET':
        return jsonify(item.to_dict())
    elif request.method == 'PUT':
        data = request.get_json()
        updated_item = services.update_item(item, data)
        return jsonify(updated_item.to_dict())
    elif request.method == 'DELETE':
        services.delete_item(item)
        return '', 204

@bp.route('/item_list', methods=['GET', 'POST'])
def item_list():
    if request.method == 'POST':
        item_id = request.form.get('ItemID')
        name = request.form['Name']
        item_type = request.form['Type']
        description = request.form['Description']
        equipped = request.form['Equipped']
        count = request.form['Count']

        if item_id:
            item = services.get_item_by_id(item_id)
            if item:
                data = {
                    'Name': name,
                    'Type': item_type,
                    'Description': description,
                    'Equipped': equipped,
                    'Count': count
                }
                services.update_item(item, data)
        else:
            data = {
                'Name': name,
                'Type': item_type,
                'Description': description,
                'Equipped': equipped,
                'Count': count
            }
            services.create_item(data)

        return redirect(url_for('routes.item_list'))

    items = services.get_all_items()
    return render_template('items.html', items=items)

@bp.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        item_type = request.form['type']
        description = request.form['description']
        equipped = request.form['equipped']
        count = request.form['count']
        character_id = request.form['character_id']
        location_id = request.form['location_id']

        data = {
            'Name': name,
            'Type': item_type,
            'Description': description,
            'Equipped': equipped,
            'Count': count,
            'CharacterID': character_id,
            'LocationID': location_id
        }
        services.create_item(data)
        return redirect(url_for('routes.item_list'))

    return render_template('add_item.html')

@bp.route('/characters/<int:character_id>/item_list', methods=['GET'])
def character_item_list(character_id):
    character = services.get_character_by_id(character_id)
    if character:
        items = character.items
        return render_template('character_items.html', character=character, items=items)
    else:
        return "Character not found", 404

# History Routes
@bp.route('/history', methods=['GET', 'POST'])
def handle_history():
    if request.method == 'GET':
        history = services.get_all_history()
        return jsonify([hist.to_dict() for hist in history])
    elif request.method == 'POST':
        data = request.get_json()
        new_history = services.create_history(data)
        return jsonify(new_history.to_dict()), 201

@bp.route('/history/<int:history_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_history_entry(history_id):
    history_entry = services.get_history_by_id(history_id)
    if not history_entry:
        return jsonify({'message': 'History entry not found'}), 404

    if request.method == 'GET':
        return jsonify(history_entry.to_dict())
    elif request.method == 'PUT':
        data = request.get_json()
        updated_history_entry = services.update_history(history_entry, data)
        return jsonify(updated_history_entry.to_dict())
    elif request.method == 'DELETE':
        services.delete_history(history_entry)
        return '', 204

# Extra Routes
@bp.route('/characters/<int:character_id>/items')
def get_character_items(character_id):
    character = services.get_character_by_id(character_id)
    if not character:
        return jsonify({'message': 'Character not found'}), 404
    items = character.items
    return jsonify([item.to_dict() for item in items])

@bp.route('/locations/<int:location_id>/characters')
def get_location_characters(location_id):
    location = services.get_location_by_id(location_id)
    if not location:
        return jsonify({'message': 'Location not found'}), 404
    characters = location.characters
    return jsonify([char.to_dict() for char in characters])