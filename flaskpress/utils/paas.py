# coding: utf-8

from shiftpy.wsgi_utils import envify


def activate(app):
    envify(app)
    return app
