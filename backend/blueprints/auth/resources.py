import hashlib
from flask import Blueprint
from flask_jwt_extended import create_access_token, get_jwt_claims, get_jwt_identity, jwt_required
from flask_restful import Api, Resource, marshal, reqparse
from blueprints import db, user_required
from blueprints.auth.model import Users

bp_auth = Blueprint("auth", __name__)
api = Api(bp_auth)

class LoginResource(Resource):
    """
    A class used to contain user's action to login

    Methods
    -------
    options(id=None)
        Return status ok when get hit
    post()
        Check user's input and create token
    """

    def options(self, id=None):
        return {"status": "ok"}, 200

    def post(self):
        """
        Check user's input (email and password) and create token
        Return 401 if user's input false or not in database

        JSON Inputs
        -----------
        email : str
            User's email
        password : str
            User's password
        """
        parser = reqparse.RequestParser()
        parser.add_argument("email", location="json", required=True)
        parser.add_argument("password", location="json", required=True)
        args = parser.parse_args()
        test_password = hashlib.md5(args["password"].encode()).hexdigest()
        qry = Users.query.filter_by(email=args["email"]).filter_by(password=test_password)
        user_data = qry.first()
        if user_data is not None:
            user_data = marshal(user_data, Users.jwt_claim_fields)
            token = create_access_token(identity=user_data["email"], user_claims=user_data)
            return {"token": token}, 200, {"Content-Type": "application/json"}
        else:
            return {"status": "UNAUTHORIZED"}, 401, {"Content-Type": "application/json"}

class SignupResource(Resource):
    """
    A class used to contain user's action to signup

    Methods
    -------
    options(id=None)
        Return status ok when get hit
    post()
        Check user's input, add to database, and create token
    """
    def options(self, id=None):
        return {"status": "ok"}, 200

    def post(self):
        """
        Check user's input (email and password), add to database, and create token
        Return 401 if user's input is false

        JSON Inputs
        -----------
        email : str
            User's email
        password : str
            User's password
        """
        parser = reqparse.RequestParser()
        parser.add_argument("email", location="json", required=True)
        parser.add_argument("password", location="json", required=True)
        args = parser.parse_args()
        ### CREATE NEW OBJECT ###
        password_digest = hashlib.md5(args["password"].encode()).hexdigest()
        user = Users(
            email=args["email"],
            password=password_digest
        )
        db.session.add(user)
        db.session.commit()
        ### CREATE TOKEN FOR AUTOMATIC LOGIN ###
        qry = Users.query.filter_by(email=args["email"]).filter_by(password=password_digest)
        user_data = qry.first()
        if user_data is not None:
            user_data = marshal(user_data, Users.jwt_claim_fields)
            token = create_access_token(identity=user_data["email"], user_claims=user_data)
            return {"token": token}, 200, {"Content-Type": "application/json"}
        else:
            return {"status": "UNAUTHORIZED"}, 401, {"Content-Type": "application/json"}

api.add_resource(LoginResource, "/login")
api.add_resource(SignupResource, "/signup")
