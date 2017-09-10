# -*- coding: utf-8 -*-

from __future__ import print_function
import logging
from flask import url_for

logger = logging.getLogger()

try:
    from flask_weasyprint import render_pdf

    import_error = False
except (ImportError, OSError) as e:
    import_error = True


def configure(app):
    if app.config.get('ENABLE_TO_PDF', False) and not import_error:

        def render_to_pdf(long_slug):
            return render_pdf(url_for('flaskpress.core.detail',
                                      long_slug=long_slug))

        app.add_flaskpress_url_rule('/<path:long_slug>.pdf',
                                view_func=render_to_pdf)
