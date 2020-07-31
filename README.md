# authenticator-sample

## Instructions

1. Install [Docker](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/) if you don't already have them installed.
2. Build and run the application by running ```docker-compose up -d``` in a terminal as a super-user.
3. Connect to the web front-end by accessing ```http://localhost:8080```.

## Architecture

As this is a reflection of a production set-up, a minimal configuration and production platform is used. Specifically, Python with Flask runs the WSGI application, with Gunicorn used as a production server. Nginx acts as a reverse proxy, forwarding traffic to the WSGI application.

The application is entirely Docker-ized and fairly modular - new services can easily be added by modyfing `docker-compose.yml` and/or editing the nginx template config file in `nginx/nginx.conf`, along with its Dockerfile to perform environment variable substitution if needed.

For the requirements given, this particular front end is simple HTML and CSS with Jinja templating. The CSS is managed by Sass, which watches `app/sass/style.scss` and compiles it to `app/static/style.css`. The HTML templates and static files are passed to the container as volumes. The other files, such as `requirements.txt` and `app.py` are copied directly on build, as specified in `app/Dockerfile`.
