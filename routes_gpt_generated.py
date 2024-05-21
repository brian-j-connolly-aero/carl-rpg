from flask import Blueprint, jsonify, request, render_template, redirect, url_for
import services
import models
from sqlalchemy.inspection import inspect

bp = Blueprint('routes', __name__)

def get_model_and_instance(model_name, instance_id=None):
    model = getattr(models, model_name, None)
    if not model:
        return None, None
    instance = services.get_by_id(model, instance_id) if instance_id else None
    return model, instance

def to_dict(instance):
    return {c.key: getattr(instance, c.key) for c in inspect(instance).mapper.column_attrs}

# Generic routes for all models
@bp.route('/<model_name>', methods=['GET', 'POST'])
def handle_models(model_name):
    model, _ = get_model_and_instance(model_name)
    if not model:
        return jsonify({'message': f'Model {model_name} not found'}), 404

    if request.method == 'GET':
        entries = services.get_all(model)
        return jsonify([to_dict(entry) for entry in entries])
    elif request.method == 'POST':
        data = request.get_json()
        new_entry = services.create(model, data)
        return jsonify(to_dict(new_entry)), 201

@bp.route('/<model_name>/<int:instance_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_model_instance(model_name, instance_id):
    model, instance = get_model_and_instance(model_name, instance_id)
    if not model or not instance:
        return jsonify({'message': f'{model_name} instance not found'}), 404

    if request.method == 'GET':
        return jsonify(to_dict(instance))
    elif request.method == 'PUT':
        data = request.get_json()
        updated_instance = services.update(instance, data)
        return jsonify(to_dict(updated_instance))
    elif request.method == 'DELETE':
        services.delete(instance)
        return '', 204

# Specific HTML routes for rendering templates
@bp.route('/<model_name>_list', methods=['GET', 'POST'])
def model_list(model_name):
    model, _ = get_model_and_instance(model_name)
    if not model:
        return jsonify({'message': f'Model {model_name} not found'}), 404

    if request.method == 'POST':
        instance_id = request.form.get(f'{model_name}ID')
        data = {key: request.form[key] for key in request.form.keys()}
        
        if instance_id:
            instance = services.get_by_id(model, instance_id)
            if instance:
                services.update(instance, data)
        else:
            services.create(model, data)
        
        return redirect(url_for(f'routes.{model_name}_list'))
    
    entries = services.get_all(model)
    return render_template(f'{model_name}.html', entries=entries)

@bp.route('/new_<model_name>', methods=['GET'])
def new_model(model_name):
    return render_template(f'add_{model_name}.html')

@bp.route('/add_<model_name>', methods=['GET', 'POST'])
def add_model(model_name):
    if request.method == 'POST':
        data = {key: request.form[key] for key in request.form.keys()}
        model, _ = get_model_and_instance(model_name)
        services.create(model, data)
        return redirect(url_for(f'routes.{model_name}_list'))
    return render_template(f'add_{model_name}.html')

@bp.route('/<model_name>/<int:instance_id>/sheet', methods=['GET'])
def model_sheet(model_name, instance_id):
    model, instance = get_model_and_instance(model_name, instance_id)
    if not model or not instance:
        return "Instance not found", 404
    return render_template(f'{model_name}_sheet.html', instance=instance)

# Extra routes for specific relationships
@bp.route('/characters/<int:character_id>/items')
def get_character_items(character_id):
    character = services.get_character_by_id(character_id)
    if not character:
        return jsonify({'message': 'Character not found'}), 404
    items = character.items
    return jsonify([to_dict(item) for item in items])

@bp.route('/locations/<int:location_id>/characters')
def get_location_characters(location_id):
    location = services.get_location_by_id(location_id)
    if not location:
        return jsonify({'message': 'Location not found'}), 404
    characters = location.characters
    return jsonify([to_dict(char) for char in characters])
