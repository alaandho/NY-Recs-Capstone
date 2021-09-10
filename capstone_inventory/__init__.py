from flask import Flask
from config import Config
from .site.routes import site
from .api.routes import api
from .authentication.routes import auth
from .models import db, login_manager
from flask_migrate import Migrate
from .helpers import JSONEncoder
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

app.config.from_object(Config)
app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)
db.init_app(app)
login_manager.init_app(app)

login_manager.login_view = 'auth.signin'

migrate = Migrate(app, db)

app.json_encoder = JSONEncoder