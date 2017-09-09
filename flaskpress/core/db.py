#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_mongoengine import Document, DynamicDocument, BaseQuerySet, MongoEngine
from flaskpress.core.fields import ListField


class FlaskQuerySet(BaseQuerySet):
    def get_or_create(self, write_options=None, auto_save=True, *q_objs, **query):
        defaults = query.get('defaults', {})
        if 'defaults' in query:
            del query['defaults']

        try:
            doc = self.get(*q_objs, **query)
            return doc, False
        except self._document.DoesNotExist:
            query.update(defaults)
            doc = self._document(**query)

            if auto_save:
                doc.save(write_options=write_options)
            return doc, True


class FlaskDocument(Document):
    meta = {'abstract': True, 'queryset_class': FlaskQuerySet}


class FlaskDynamicDocument(DynamicDocument):
    meta = {'abstract': True, 'queryset_class': FlaskQuerySet}


db = MongoEngine()
db.ListField = ListField
db.Document = FlaskDocument
db.DynamicDocument = FlaskDynamicDocument