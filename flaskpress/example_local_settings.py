# coding: utf-8

# MONGO
MONGODB_DB = "flaskpress_db"
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_USERNAME = None
MONGODB_PASSWORD = None

# Debug and toolbar
DEBUG = True
DEBUG_TOOLBAR_ENABLED = False


# set this to true in development mode
if DEBUG:
    ADMIN_RAISE_ON_VIEW_EXCEPTION = True


# locale
BABEL_DEFAULT_LOCALE = 'en'

# Logger
LOGGER_ENABLED = True
LOGGER_LEVEL = 'DEBUG'
LOGGER_FORMAT = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
LOGGER_DATE_FORMAT = '%d.%m %H:%M:%S'
