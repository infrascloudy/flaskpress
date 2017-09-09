#!/usr/bin/env python
# -*- coding: utf-8 -*
from werkzeug.utils import import_string
from flask_admin import Admin

from flaskpress.core.models.channel import Channel, ChannelType
from flaskpress.core.models.config import Config
from flaskpress.core.models.content import Link, ContentTemplateType
from flaskpress.core.models.subcontent import SubContentPurpose
from flaskpress.utils.translation import _l, _n
from flaskpress.utils.settings import get_setting_value

from flaskpress.core.admin.models import ModelAdmin, FileAdmin, BaseIndexView
from flaskpress.core.admin.views import IndexView, InspectorView, LinkAdmin, ConfigAdmin, SubContentPurposeAdmin, ChannelTypeAdmin, ContentTemplateTypeAdmin
from flaskpress.core.admin.views import ChannelAdmin


_n  # noqa


class FlaskpressAdmin(Admin):
    registered = []

    def register(self, model, view=None, *args, **kwargs):
        _view = view or ModelAdmin
        admin_view_exclude = get_setting_value('ADMIN_VIEW_EXCLUDE', [])
        identifier = '.'.join((model.__module__, model.__name__))
        if (identifier not in admin_view_exclude) and (
                identifier not in self.registered):
            self.add_view(_view(model, *args, **kwargs))
            self.registered.append(identifier)


def create_admin(app=None):
    index_view = IndexView()
    return FlaskpressAdmin(app, index_view=index_view)


def configure_admin(app, admin):  # noqa

    custom_index = app.config.get('ADMIN_INDEX_VIEW')
    if custom_index:
        admin.index_view = import_string(custom_index)()
        if isinstance(admin._views[0], BaseIndexView):
            del admin._views[0]
        admin._views.insert(0, admin.index_view)

    admin_config = app.config.get(
        'ADMIN',
        {
            'name': 'Flaskpress Admin',
            'url': '/admin'
        }
    )

    for k, v in list(admin_config.items()):
        setattr(admin, k, v)

    for entry in app.config.get('FILE_ADMIN', []):
        try:
            admin.add_view(
                FileAdmin(
                    entry['path'],
                    entry['url'],
                    name=_l(entry['name']),
                    category=_l(entry['category']),
                    endpoint=entry['endpoint'],
                    roles_accepted=entry.get('roles_accepted'),
                    editable_extensions=entry.get('editable_extensions')
                )
            )
        except Exception as e:
            app.logger.info(e)

    for k, theme in app.theme_manager.themes.items():
        try:

            if k == app.config.get('DEFAULT_THEME'):
                suffix = "(Site theme)"
            elif k == app.config.get('ADMIN_THEME'):
                suffix = "(Admin theme)"
            else:
                suffix = "Theme"

            admin.add_view(
                FileAdmin(
                    theme.static_path,
                    "/_themes/{0}/".format(theme.identifier),
                    name="{0}: {1} static files".format(suffix,
                                                        theme.identifier),
                    category=_l("Files"),
                    endpoint="{0}_static_files".format(theme.identifier),
                    roles_accepted=('admin', "editor"),
                    editable_extensions=app.config.get(
                        'DEFAULT_EDITABLE_EXTENSIONS')
                )
            )
            admin.add_view(
                FileAdmin(
                    theme.templates_path,
                    "/theme_template_files/{0}/".format(theme.identifier),
                    name="{0}: {1} template files".format(suffix,
                                                          theme.identifier),
                    category=_l("Files"),
                    endpoint="{0}_template_files".format(theme.identifier),
                    roles_accepted=('admin', "editor"),
                    editable_extensions=app.config.get(
                        'DEFAULT_EDITABLE_EXTENSIONS')
                )
            )
        except Exception as e:
            app.logger.warning(
                'Error registering %s folder to file admin %s' % (
                    theme.identifier, e
                )
            )

    admin.add_view(InspectorView(category=_l("Settings"),
                                 name=_l("Inspector")))

    extra_views = app.config.get('ADMIN_EXTRA_VIEWS', [])
    for view in extra_views:
        admin.add_view(
            import_string(view['module'])(
                category=_l(view.get('category')),
                name=_l(view.get('name'))
            )
        )

    admin.register(
        Link,
        LinkAdmin,
        category=_l("Content"),
        name=_l("Link")
    )
    admin.register(Config,
                   ConfigAdmin,
                   category=_l("Settings"),
                   name=_l("Config"))
    admin.register(SubContentPurpose,
                   SubContentPurposeAdmin,
                   category=_l("Settings"),
                   name=_l("Sub content purposes"))
    admin.register(ChannelType, ChannelTypeAdmin,
                   category=_l("Settings"), name=_l("Channel type"))
    admin.register(ContentTemplateType,
                   ContentTemplateTypeAdmin,
                   category=_l("Settings"),
                   name=_l("Template type"))
    admin.register(Channel, ChannelAdmin,
                   category=_l("Content"), name=_l("Channel"))

    # avoid registering twice
    if admin.app is None:
        admin.init_app(app)

    return admin
