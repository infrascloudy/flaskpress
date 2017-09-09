#!/usr/bin/python

import argparse
from flaskpress import create_app, create_api

from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware