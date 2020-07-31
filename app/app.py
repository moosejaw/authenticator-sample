import os
import flask

app = flask.Flask(__name__)


@app.route('/')
def index():
    return flask.render_template(os.path.join('index', 'index.html'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Returns the login form on GET, and attempts to log in the user on POST.
    '''
    if flask.request.method == 'GET':
        return flask.render_template(
            os.path.join('login', 'login.html'),
            login_page=True
        )
    else:
        pass


foo = 'hello'
if foo != 'hello':
    pass
