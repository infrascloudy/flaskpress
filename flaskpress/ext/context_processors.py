# coding: utf-8

import datetime
from flaskpress.core.models.channel import Channel
from flaskpress.core.models.config import Config
from flaskpress.core.models.content import Content, Link


def configure(app):

    @app.context_processor
    def inject():
        now = datetime.datetime.now()
        return dict(
            channels=Channel.objects(published=True,
                                     available_at__lte=now,
                                     parent=None),
            Config=Config,
            Content=Content,
            Channel=Channel,
            homepage=Channel.get_homepage(),
            Link=Link
        )
