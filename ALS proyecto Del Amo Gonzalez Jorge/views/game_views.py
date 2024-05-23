import flask
import flask_login
import sirope
from model.gamedto import GameDto
from model.userdto import UserDto
from model.reviewdto import ReviewDto
from model.commentdto import CommentDto

game_blprint = flask.Blueprint('game', __name__, url_prefix='/game')

@flask_login.login_required
@game_blprint.route('/list', methods=['GET'])
def list_games():
    srp = sirope.Sirope()
    search_query = flask.request.args.get('search', '').lower()

    all_games = list(srp.load_all(GameDto))
    if search_query:
        games = [game for game in all_games if search_query in game.title.lower()]
    else:
        games = all_games
    
    return flask.render_template('list_games.html', usr=UserDto.current_user(), games=games, search_query=search_query)

@flask_login.login_required
@game_blprint.route('/details/<game_id>', methods=['GET'])
def game_details(game_id):
    srp = sirope.Sirope()
    game = srp.find_first(GameDto, lambda g: g.get_id() == game_id)
    
    if not game:
        flask.flash("Juego no encontrado")
        return flask.redirect('/game/list')

    reviews = []
    for oid in game.reviews:
        review = srp.find_first(ReviewDto, lambda r: str(r.get_oid()) == str(oid))
        if review:
            reviews.append(review)
        else:
            # Eliminar la referencia a la reseña que ya no existe.
            game.reviews.remove(oid)
            srp.save(game)

    return flask.render_template('game_details.html', usr=UserDto.current_user(), game=game, reviews=reviews)

@flask_login.login_required
@game_blprint.route('/add', methods=['GET', 'POST'])
def add_game():
    if flask.request.method == 'POST':
        title = flask.request.form.get('title')
        description = flask.request.form.get('description')
        developer = flask.request.form.get('developer')
        genre = flask.request.form.get('genre')
        platform = flask.request.form.get('platform')
        user = UserDto.current_user()
        game = GameDto(title, description, developer, genre, platform, user.email)
        srp = sirope.Sirope()
        srp.save(game)
        
        oid = game.get_oid()
        stored_game = srp._redis.hget(oid.namespace, str(oid.num))
        print(f"Juego guardado con OID: {oid}")
        print(f"Objeto almacenado en Redis: {stored_game}")
        
        return flask.redirect('/game/list')
    return flask.render_template('add_game.html', usr=UserDto.current_user())

@flask_login.login_required
@game_blprint.route('/edit/<game_id>', methods=['GET', 'POST'])
def edit_game(game_id):
    srp = sirope.Sirope()
    game = srp.find_first(GameDto, lambda g: g.get_id() == game_id)
    
    if not game or game.owner_email != UserDto.current_user().email:
        flask.flash("No tiene permiso para editar este juego.")
        return flask.redirect('/game/list')
    
    if flask.request.method == 'POST':
        game.title = flask.request.form.get('title')
        game.description = flask.request.form.get('description')
        game.developer = flask.request.form.get('developer')
        game.genre = flask.request.form.get('genre')
        game.platform = flask.request.form.get('platform')
        srp.save(game)
        return flask.redirect('/game/list')
    
    return flask.render_template('edit_game.html', usr=UserDto.current_user(), game=game, game_id=game_id)

@flask_login.login_required
@game_blprint.route('/delete/<game_id>', methods=['POST'])
def delete_game(game_id):
    srp = sirope.Sirope()
    game = srp.find_first(GameDto, lambda g: g.get_id() == game_id)
    
    if not game or game.owner_email != UserDto.current_user().email:
        flask.flash("No tiene permiso para eliminar este juego.")
        return flask.redirect('/game/list')

    # Eliminar las reseñas asociadas al juego y sus comentarios
    for review_oid in game.reviews:
        review = srp.find_first(ReviewDto, lambda r: str(r.get_oid()) == str(review_oid))
        if review:
            # Eliminar comentarios asociados a la reseña
            for comment_oid in review.comments:
                comment = srp.find_first(CommentDto, lambda c: str(c.get_oid()) == str(comment_oid))
                if comment:
                    srp.delete(comment.get_oid())
            
            # Eliminar la reseña
            srp.delete(review.get_oid())

    # Eliminar el juego
    srp.delete(game.get_oid())
    flask.flash("Juego, sus reseñas y comentarios eliminados con éxito.")
    return flask.redirect('/game/list')

