#need to handle db reset properly
# Create routing to display page with character as plain text
# Add item/ItemID routing
# Define separate function outside of route with **kwargs to return formatted character update


from flask import Flask
from config import Config
import models



def create_app():
    app = Flask(__name__, template_folder='html')
    app.config.from_object(Config)
    models.db.init_app(app)

    # Import and register blueprints
    from routes_gpt_generated import bp as routes_bp
    app.register_blueprint(routes_bp)
    with app.app_context():
        models.db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
    