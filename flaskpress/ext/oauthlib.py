# coding utf-8

from flask import session
from flask_oauthlib.client import OAuth

from flaskpress.modules.accounts.oauth import make_oauth_handler, oauth_login


def configure(app):
    app.add_flaskpress_url_rule('/accounts/oauth/login/<provider>/', 'oauth_login', oauth_login)

    config = app.config.get("OAUTH")
    if not config:
        return

    oauth = OAuth(app)

    for provider, data in config.items():
        provider_name = "oauth_" + provider
        oauth_app = oauth.remote_app(
            provider,
            **{k: v for k, v in data.items() if not k.startswith("_")}
        )

        token_var = "oauth_{}_token".format(provider)
        oauth_app.tokengetter(lambda: session.get(token_var))

        setattr(app, provider_name, oauth_app)

        app.add_flaskpress_url_rule(
            '/accounts/oauth/authorized/{0}/'.format(provider),
            '{0}_authorized'.format(provider),
            oauth_app.authorized_handler(make_oauth_handler(provider))
        )

        if provider == 'linkedin':
            def change_linkedin_query(uri, headers, body):
                auth = headers.pop('Authorization')
                headers['x-li-format'] = 'json'
                if auth:
                    auth = auth.replace('Bearer', '').strip()
                    if '?' in uri:
                        uri += '&oauth2_access_token=' + auth
                    else:
                        uri += '?oauth2_access_token=' + auth
                return uri, headers, body

            oauth_app.pre_request = change_linkedin_query
