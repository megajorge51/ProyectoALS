import json
import flask
import flask_login
import sirope
from views.user_views import user_blprint
from views.game_views import game_blprint
from views.review_views import review_blprint
from views.comment_views import comment_blprint
from model.userdto import UserDto

def create_app():
    app = flask.Flask(__name__, instance_relative_config=True)
    app.config.from_file("config.json", load=json.load)
    login_manager = flask_login.LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'index'

    @login_manager.user_loader
    def load_user(email):
        return UserDto.find(sirope.Sirope(), email)

    app.register_blueprint(user_blprint)
    app.register_blueprint(game_blprint)
    app.register_blueprint(review_blprint)
    app.register_blueprint(comment_blprint)

    @app.route('/')
    def index():
        usr = UserDto.current_user()
        return flask.render_template('index.html', usr=usr)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
