# coding: utf-8

from flaskpress_themes import Themes


def configure(app):
    themes = Themes()
    themes.init_themes(app, app_identifier="flaskpress")
