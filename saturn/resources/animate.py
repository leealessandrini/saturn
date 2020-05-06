"""
Animation Resource

Description:
This resource will house the requests to create and retrieve video animations.
"""
from io import BytesIO
from flask import send_file
from flask_restx import Resource, reqparse
from werkzeug.datastructures import FileStorage

from saturn.apis import api
from saturn.common import animation

parser = reqparse.RequestParser()
parser.add_argument(
    'audio', location='files', type=FileStorage, required=True)
parser.add_argument(
    'image', location='files', type=FileStorage, required=True)
parser.add_argument(
    'title', type=str, required=False)


@api.expect(parser)
class Animate(Resource):

    def post(self):
        """
			Create spectrum animation provided audio and image files.
        """
        args = parser.parse_args()
        print(args)
        # Create animation
        animation.create_animation(
        	args["audio"], args["image"], args["title"])

        return send_file(
        	BytesIO(open("output.mp4", "rb").read()),
        	as_attachment=True,
        	attachment_filename="animation.mp4")