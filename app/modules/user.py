from flask_login import UserMixin


class User(UserMixin):
    '''
    Represents a user inside of a Flask session.

    Inherits from flask_login.UserMixin, thereby containing all
    the necessary attributes for flask_login to work correctly.

    The key difference here is that the JWT returned from the authenticator
    container and the user ID are required in the constructor.

    Params:
        - token: String containing the token provided by the authenticator
        container.
        - id: The username corresponding to the user logged in.'''
    def __init__(self, token, id):
        self._token = token
        self._id = u'{}'.format(id)

    @property
    def token(self):
        return self._token

    @property
    def id(self):
        return self._id

    def get_id(self):
        '''Quick implementation for flask-login.'''
        return self.id
