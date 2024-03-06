#need to handle db reset properly
# Create routing to display page with character as plain text
# Add item/ItemID routing
# Define separate function outside of route with **kwargs to return formatted character update


from flask import Flask
from config import Config
from models import Party, Floor, Location, Character, Item, History, db
#from routes import characters

def create_app():
    app = Flask(__name__, template_folder='html')
    app.config.from_object(Config)
    db.init_app(app)

    # Import and register blueprints
    from routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)