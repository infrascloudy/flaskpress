# coding: utf-8
def expose(url='/', methods=('GET',)):
    def wrap(f):
        if not hasattr(f, '_urls'):
            f._urls = []
        f._urls.append((url, methods))
        return f

    return wrap
