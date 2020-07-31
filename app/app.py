import os
import flask

app = flask.Flask(__name__)


@app.route("/")
def index():
    return flask.render_template("www/index.html")


if __name__ == '__main__':
    app.run(port=os.environ['PORT'])
