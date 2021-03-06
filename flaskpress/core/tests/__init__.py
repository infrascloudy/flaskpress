# coding: utf-8
from flask_testing import TestCase

from flaskpress import create_app
from flaskpress.core.admin import create_admin


class BaseTestCase(TestCase):
    def create_app(self):
        self.admin = create_admin()
        return create_app(config='flaskpress.test_settings',
                          admin_instance=self.admin,
                          test=True)
