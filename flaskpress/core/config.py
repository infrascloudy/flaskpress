import os
import logging
import flaskpress.core.models as m
from flask.config import Config
from flaskpress.utils import parse_conf_data
from cached_property import cached_property_ttl, cached_property

logger = logging.getLogger()


class FlaskpressConfig(Config):
    @cached_property
    def store(self):
        return dict(self)

    @cached_property_ttl(300)
    def all_setings_from_db(self):
        try:
            return {item.name: item.value for item in m.config.Config.objects.get(group='settings').values}
        except Exception as e:
            logger.warning('Error reading all settings from db: %s' % e)
            return {}

    def get_from_db(self, key, default=None):
        return self.all_setings_from_db.get(key, default)

    def __getitem__(self, key):
        return self.get_from_db(key) or dict.__getitem__(self, key)

    def get(self, key, default=None):
        return self.get_from_db(key) or self.store.get(key) or default

    def from_object(self, obj, silent=False):
        try:
            super(FlaskpressConfig, self).from_object(obj)
        except ImportError as e:
            if silent:
                return False
            e.message = 'Unable to load configuration obj (%s)' % e.message
            raise

    def from_envvar_namespace(self, namespace='FLASKPRESS', silent=False):
        try:
            data = {
                key.partition('_')[-1]: parse_conf_data(data)
                for key, data
                in os.environ.items()
                if key.startswith(namespace)
            }
            self.update(data)
        except Exception as e:
            if silent:
                return False
            e.message = 'Unable to load config env namespace (%s)' % e.message
            raise

    def load_flaskpress_config(self, config=None, mode=None, test=None, **sets):
        self.from_object(config or 'flaskpress.settings')
        mode = mode or 'test' if test else os.environ.get(
            'FLASKPRESS_MODE', 'local')
        self.from_object('flaskpress.%s_settings' % mode, silent=True)
        path = "FLASKPRESS_SETTINGS" if not test else "FLASKPRESSTEST_SETTINGS"
        self.from_envvar(path, silent=True)
        self.from_envvar_namespace(namespace='FLASKPRESS', silent=True)
        self.update(sets)
