import flask
import flask_login
import sirope
from model.userdto import UserDto

user_blprint = flask.Blueprint('user', __name__, url_prefix='/user')

@user_blprint.route('/add', methods=['POST'])
def add_user():
    email = flask.request.form.get("edEmail")
    pswd = flask.request.form.get("edPswd")
    if not email or not pswd:
        flask.flash("Email y contraseña son requeridos")
        return flask.redirect("/")

    srp = sirope.Sirope()
    if UserDto.find(srp, email):
        flask.flash("Usuario ya existente")
        return flask.redirect("/")

    usr = UserDto(email, pswd)
    srp.save(usr)
    flask.flash("Usuario registrado con éxito. Por favor, inicie sesión.")
    return flask.redirect("/")

@user_blprint.route('/login', methods=['POST'])
def login():
    email = flask.request.form.get("edEmail")
    pswd = flask.request.form.get("edPswd")

    srp = sirope.Sirope()
    usr = UserDto.find(srp, email)
    if not usr or not usr.chk_password(pswd):
        flask.flash("Email o contraseña incorrectos")
        return flask.redirect("/")

    flask_login.login_user(usr)
    return flask.redirect("/")

@user_blprint.route('/logout')
def logout():
    flask_login.logout_user()
    return flask.redirect("/")
