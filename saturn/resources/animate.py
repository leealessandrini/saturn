"""
Animation Resource

Description:
This resource will house the requests to create and retrieve video animations.
"""
from flask_restx import Resource, reqparse
from werkzeug.datastructures import FileStorage

from saturn.apis import api

parser = reqparse.RequestParser()
parser.add_argument(
    'audio', location='files', type=FileStorage, required=True)
parser.add_argument(
    'image', location='files', type=FileStorage, required=True)


@api.expect(parser)
class Animate(Resource):

    def post(self):
        """

        """
        args = parser.parse_args()

        return "Sgo birds"