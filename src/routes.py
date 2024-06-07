from flask import Blueprint, Request, Response, json
from src.controllers.auth_controller import auth
api = Blueprint('api',__name__)

api.register_blueprint(auth,url_prefix='/auth')