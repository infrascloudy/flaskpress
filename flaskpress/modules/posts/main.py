#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flaskpress.core.app import FlaskpressModule

module = FlaskpressModule('posts', __name__, template_folder='templates')
