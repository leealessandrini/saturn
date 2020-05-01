"""
Lee Alessandrini
Saturn Backend API
"""
import os
from flask import Flask
from saturn.config import DevelopmentConfig

def create_app(script_info=None):
    """
    """

    # Instantiate application
    app = Flask(__name__)

    # Setup application config
    app_settings = os.getenv("APP_SETTINGS")

    if app_settings == 'Development':
        app.config.from_object(DevelopmentConfig)

    # Register API's
    from .apis import blueprint
    app.register_blueprint(blueprint)

    # Shell context for flask cli
    app.shell_context_processor({"app": app})

    return app