from flask import Flask, Blueprint
from flask.helpers import _endpoint_from_view_func
from flaskpress.core.config import FlaskpressConfig
from flaskpress.utils.aliases import dispatch_aliases


class FlaskpressApp(Flask):
    config_class = FlaskpressConfig

    def make_config(self, instance_relative=False):
        root_path = self.root_path
        if instance_relative:
            root_path = self.instance_path
        return self.config_class(root_path, self.default_config)

    def preprocess_request(self):
        return dispatch_aliases() or super(FlaskpressApp, self).preprocess_request()

    def add_flaskpress_url_rule(self, rule, endpoint=None, view_func=None, **options):
        if endpoint is None:
            endpoint = _endpoint_from_view_func(view_func)
        if not endpoint.startswith('flaskpress.'):
            endpoint = 'flaskpress.core.' + endpoint
        self.add_url_rule(rule, endpoint, view_func, **options)


class FlaskpressModule(Blueprint):
    def __init__(self, name, *args, **kwargs):
        name = "flaskpress.modules." + name
        super(FlaskpressModule, self).__init__(name, *args, **kwargs)
