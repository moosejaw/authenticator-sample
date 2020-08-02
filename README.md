# authenticator-sample

## Instructions

1. Install [Docker](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/) if you don't already have them installed. Make sure the Docker service is running and the `docker-compose` executable is linked in your PATH.
2. Clone this repository, and `cd` to the repo folder in a terminal.
3. Build and run the application by running ```docker-compose up -d``` as a super-user.
4. Connect to the web front-end by accessing ```http://localhost:8080``` in a browser.

## Tools/Libraries Used

- Docker and Docker Compose
- Flask and flask-login
- Gunicorn
- SASS
- Nginx

## Explanation

As this is a reflection of a production set-up, a minimal configuration and production platform is used. Specifically, Python with Flask runs the WSGI application, with Gunicorn used as a production server. Nginx acts as a reverse proxy, forwarding traffic to the web app.

The application is entirely Docker-ized and fairly modular - new services can easily be added by modyfing `docker-compose.yml` and/or editing the nginx template config file in `nginx/nginx.conf`, along with its Dockerfile to perform environment variable substitution if needed.

For the requirements given, this particular front end is simple HTML and CSS with Jinja templating. The CSS is managed by Sass, which watches `app/sass/style.scss` and compiles it to `app/static/style.css`. The HTML templates and static files are passed to the container as volumes. The other files, such as `requirements.txt` and `app.py` are copied directly on build, as specified in `app/Dockerfile`.

The [authentication service](https://github.com/dantame/interview-authentication-service) repo is run in the `auth` container defined in the compose file. It is simply a Node image which `git clone`s the repository, installs the requirements and runs it normally. The login functionality is simply just a POST request from the user/password form which gets sent to the authentication service.

## Improvements

For a true-to-life production setting, there are various improvements which can be made:

- User sessions are stored in a dict variable and are therefore unique to each Gunicorn worker. As flask-login requires the actual User instance when checking if a user is logged in, it would be better to use a database of some kind where a (verified) `pickle`d representation of the User instance is stored in a `session` table where the user ID is the key and the instance data is stored in another field as bytes. The user can be deleted from the `session` table when their session expires and the `user_loader` behaviour can be modified to support this.
  - Maybe JSON would be safer if the User object gets manually reconstructed.

- The Nginx config file would need more production-ready settings (such as a non-sudo user, etc.)

- Nginx logging.

- Add tags and other labels to Dockerfiles.
