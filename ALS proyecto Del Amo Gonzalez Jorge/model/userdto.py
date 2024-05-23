import sirope
import flask_login
import werkzeug.security as safe

class UserDto(flask_login.UserMixin):
    def __init__(self, email, password):
        self._email = email
        self._password = safe.generate_password_hash(password)

    @property
    def email(self):
        return self._email

    def get_id(self):
        return self.email

    def chk_password(self, pswd):
        return safe.check_password_hash(self._password, pswd)

    @staticmethod
    def current_user():
        usr = flask_login.current_user

        if usr.is_anonymous:
            flask_login.logout_user()
            usr = None

        return usr

    @staticmethod
    def find(s: sirope.Sirope, email: str) -> "UserDto":
        return s.find_first(UserDto, lambda u: u.email == email)
