# coding: utf-8
from flaskpress.core.templates import render_template


def configure(app):
    @app.errorhandler(403)
    def forbidden_page(*args, **kwargs):
        return render_template("errors/access_forbidden.html"), 403

    @app.errorhandler(404)
    def page_not_found(*args, **kwargs):
        return render_template("errors/page_not_found.html"), 404

    @app.errorhandler(405)
    def method_not_allowed_page(*args, **kwargs):
        return render_template("errors/method_not_allowed.html"), 405

    @app.errorhandler(500)
    def server_error_page(*args, **kwargs):
        return render_template("errors/server_error.html"), 500

    def admin_icons_error_handler(error, endpoint, *args, **kwargs):
        if endpoint in [item[0] for item in app.config.get('ADMIN_ICONS', [])]:
            return '/admin'
        raise error

    app.url_build_error_handlers.append(admin_icons_error_handler)
