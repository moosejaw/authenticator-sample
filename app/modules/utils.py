import os
import flask
import requests
import flask_login


def verify_user_token(session, user=flask_login.current_user):
    '''
    If a user is logged in according to flask-login, this function calls the
    /verifyToken endpoint of the auth container to check the user's JWT is
    still valid and logs them out if not (they also get logged out if they
    have no token, or don't exist in the session dict).

    In practice, this would be called on every page that needed a user to
    be logged in.

    Params:
        - session: the user_sessions lookup dict from the app.

    Keywords:
        - user: flask_login.current_user instance (the currently logged
        in user who's token is being checked).
    '''
    def logout_and_redirect():
        '''Logs the user out and calls a flask redirect
        back to the index page.'''
        flask_login.logout_user()
        return flask.redirect(flask.url_for('index'))

    try:
        token = session[user.id].token
    except AttributeError:
        return logout_and_redirect()
    except KeyError:
        return logout_and_redirect()

    try:
        res = requests.get(
            f'http://{os.environ["AUTH_DNS"]}:'
            f'{os.environ["AUTH_PORT"]}/verifyToken',
            headers={'Authorization': f'Bearer {token}'}
        )
    except requests.exceptions.ConnectionError:
        # Should write to a log here
        return logout_and_redirect()
    else:
        if res.status_code == 200:
            # All good
            return
        else:
            # Log here too
            return logout_and_redirect()
