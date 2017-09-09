#!/usr/bin/env python
# -*- coding: utf-8 -*-
import warnings
from flask.exthook import ExtDeprecationWarning
from flaskpress.core.admin import create_admin

warnings.simplefilter("ignore", category=ExtDeprecationWarning)

admin = create_admin()