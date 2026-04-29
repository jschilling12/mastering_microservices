from application import create_app, db
from application import models
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, models.db)

from flask import g
from flask.sessions import SecureCookieSessionInterface
from flask_login import user_loaded_from_request


@user_loaded_from_request.connect
def user_loaded_from_request(app, user=None):
    g.login_via_request = True


class CustomSessionInterface(SecureCookieSessionInterface):
    """Prevent creating session from API requests."""
    def save_session(self, *args, **kwargs):
        if g.get('login_via_request'):
            return
        return super(CustomSessionInterface, self).save_session(*args,
                                                                **kwargs)

app.session_interface = CustomSessionInterface()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)