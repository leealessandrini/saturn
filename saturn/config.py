"""
Flask application configuration
"""

class BaseConfig(object):
	""" Base Configuration """

	WTF_CSRF_ENABLED = True


class DevelopmentConfig(BaseConfig):
	""" Development """

	WTF_CSRF_ENABLED = False