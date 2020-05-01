from flask import Blueprint
from flask_restx import Api


# Initialize rest api with flask blueprint
blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(
	blueprint, version='1.0', title='Saturn Rest API',
	description='Saturn Video Effects Generation API')