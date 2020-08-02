import os
import flask
import requests
import markupsafe
import flask_login
from modules.user import User
from modules.utils import verify_user_token


app = flask.Flask(__name__)
app.secret_key = os.urandom(16)  # disposable key for convenience sake
login_mgr = flask_login.LoginManager()
login_mgr.init_app(app)

session_users = {}  # stores the active user sessions


@login_mgr.user_loader
def load_user(user_id):
    if user_id is not None:
        try:
            return session_users[user_id]
        except KeyError:
            return None
    return None


@app.route('/')
def index():
    '''Renders the homepage template.'''
    return flask.render_template(os.path.join('index', 'index.html'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Returns the login form on GET, and attempts to log in the user on POST.
    '''
    def render_page(failed_login=None):
        '''
        Renders the login form in a browser. When failed is not None,
        it is a tuple containing the HTTP status code and error message
        from the failed login attempt.
        '''
        return flask.render_template(
            os.path.join('login', 'login.html'),
            failed_login=failed_login
        )

    if flask.request.method == 'GET':
        return render_page()
    else:
        res = requests.post(
            f'http://{os.environ["AUTH_DNS"]}:{os.environ["AUTH_PORT"]}/login',
            json={
                'username': flask.request.form['username'],
                'password': flask.request.form['password']
            }
        )
        if res.status_code == 200:
            # Create a new 'user', log them in with flask-login
            # and set the JWT as the 'token' property
            user_name = markupsafe.escape(flask.request.form['username'])

            # For convenience, the user_name is the same as the user_id
            # (except the user_id is converted to unicode as required by
            # flask-login)
            user = User(res.json()['token'], user_name)
            user.name = user_name
            session_users[user.id] = user
            flask_login.login_user(user)

            # Return the user to index for now
            return flask.redirect(flask.url_for('index'))
        else:
            # Non-200 from authenticator, reload login form w/ error message
            return render_page(failed_login=(res.status_code, res.text))


@app.route('/logout')
@flask_login.login_required
def logout():
    '''
    Logs a user out. Their ID is directly deleted from the user_sessions
    dictionary then the flask_login logout function is called which handles
    everything else in the background.
    '''
    verify_user_token(session_users)

    # Remove user from sessions dict
    del session_users[flask_login.current_user.id]

    # Then logout as normal
    flask_login.logout_user()
    return flask.redirect(flask.url_for('index'))
