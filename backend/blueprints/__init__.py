import json, os
from datetime import timedelta
from flask import Flask, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, get_jwt_claims, verify_jwt_in_request
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

app = Flask(__name__)
CORS(app)
app.config["APP_DEBUG"] = True

### JWT ###
app.config["JWT_SECRET_KEY"] = "SFsieaaBsLEpecP675r243faM8oSB2hV"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
jwt = JWTManager(app)

### CHECK USER'S TOKEN ###
def user_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        return fn(*args, **kwargs)
    return wrapper

### SQLALCHEMY CONFIG ###
try:
    env = os.environ.get("FLASK_ENV", "development")
    if env == "testing":
        app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:Willy_123@localhost:3306/unsircle_test_be_test"
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:Willy_123@localhost:3306/unsircle_test_be"
except Exception as e:
    raise e

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)

### AFTER REQUEST ###
@app.after_request
def after_request(response):
    try:
        myrequest = request.get_json()
    except:
        myrequest = request.args.to_dict()
    if response.status_code == 200:
        app.logger.info("REQUEST_LOG\t%s", json.dumps({
            "status_code": response.status_code,
            "method": request.method,
            "code": response.status,
            "uri": request.full_path,
            "request": myrequest,
            "response": json.loads(response.data.decode("utf-8"))
        }))
    else:
        app.logger.warning("REQUEST_LOG\t%s", json.dumps({
            "status_code": response.status_code,
            "method": request.method,
            "code": response.status,
            "uri": request.full_path,
            "request": myrequest,
            "response": json.loads(response.data.decode("utf-8"))
        }))
    return response

### IMPORT BLUEPRINTS ###
from blueprints.auth.resources import bp_auth

app.register_blueprint(bp_auth, url_prefix="/auth")

db.create_all()
