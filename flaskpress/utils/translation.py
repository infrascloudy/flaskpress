from flask import g
from babel.support import LazyProxy
from flask_babelex import gettext, lazy_gettext, ngettext

# from flaskpress.utils.translations import ugettext_lazy as _


def ugettext(s):
    return g.translations.ugettext(s)


ugettext_lazy = LazyProxy(ugettext)

_ = gettext
_l = lazy_gettext
_n = ngettext
