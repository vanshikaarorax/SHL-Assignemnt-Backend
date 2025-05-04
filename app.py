from flask import Flask
from flask_cors import CORS
from routes import main_routes
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Load config settings

    # Enable CORS for all routes
    CORS(app)  # This will enable CORS globally for the app

    # Register routes
    app.register_blueprint(main_routes)

    return app

# Expose app for gunicorn
app = create_app()

if __name__ == "__main__":
    app.run(host=app.config['HOST'], port=app.config['PORT'])
