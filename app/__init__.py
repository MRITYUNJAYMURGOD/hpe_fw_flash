from flask import Flask, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from config import Config
from .extensions import db
from celery_worker import celery
from .servers import bp as servers_bp
from .credentials import bp as credentials_bp
from .flashing import bp as flashing_bp

# import the singleton

def create_app(config_class: type = Config):
    load_dotenv()

    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(config_class)

    # Initialise extensions ONCE
    db.init_app(app)
    CORS(app)

    # Blueprint registration


    app.register_blueprint(servers_bp,   url_prefix='/api/servers')
    app.register_blueprint(credentials_bp, url_prefix='/api/credentials')
    app.register_blueprint(flashing_bp,  url_prefix='/api/flash')

    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/health')
    def health():
        return {'status': 'ok'}

    return app
