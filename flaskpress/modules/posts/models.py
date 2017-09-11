#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flaskpress.core.db import db
from flaskpress.core.models.content import Content


class Post(Content):
    # URL_NAMESPACE = 'flaskpress.modules.posts.detail'
    body = db.StringField(required=True)
