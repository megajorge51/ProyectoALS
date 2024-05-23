import flask
import flask_login
import sirope
from model.commentdto import CommentDto
from model.reviewdto import ReviewDto
from model.userdto import UserDto
from model.gamedto import GameDto

review_blprint = flask.Blueprint('review', __name__, url_prefix='/review')

@flask_login.login_required
@review_blprint.route('/add/<game_id>', methods=['GET', 'POST'])
def add_review(game_id):
    srp = sirope.Sirope()
    if flask.request.method == 'POST':
        rating = flask.request.form.get('rating')
        comment = flask.request.form.get('comment')
        if not rating or not comment.strip() or not 1 <= int(rating) <= 5:
            flask.flash("La calificación debe ser un número entre 1 y 5, y el comentario no puede estar vacío.")
            return flask.redirect(flask.url_for('review.add_review', game_id=game_id))
        user = UserDto.current_user()
        review = ReviewDto(game_id, user.email, rating, comment)
        srp.save(review)
        
        game = srp.find_first(GameDto, lambda g: g.get_id() == game_id)
        if game:
            game.reviews.append(review.get_oid())
            srp.save(game)

        return flask.redirect(f'/game/details/{game_id}')
    return flask.render_template('add_review.html', usr=UserDto.current_user(), game_id=game_id)



@flask_login.login_required
@review_blprint.route('/edit/<review_id>', methods=['GET', 'POST'])
def edit_review(review_id):
    srp = sirope.Sirope()
    review = srp.find_first(ReviewDto, lambda r: str(r.get_oid()) == review_id)

    if not review or review.reviewer_email != UserDto.current_user().email:
        flask.flash("No tienes permiso para editar esta reseña.")
        return flask.redirect('/game/list')

    if flask.request.method == 'POST':
        rating = flask.request.form.get('rating')
        comment = flask.request.form.get('comment')
        if not rating or not comment.strip():
            flask.flash("La calificación y el comentario no pueden estar vacíos.")
            return flask.redirect(flask.url_for('review.edit_review', review_id=review_id))
        review.rating = rating
        review.comment = comment
        srp.save(review)
        return flask.redirect(f'/game/details/{review.game_id}')

    return flask.render_template('edit_review.html', usr=UserDto.current_user(), review=review)


@flask_login.login_required
@review_blprint.route('/delete/<review_id>', methods=['POST'])
def delete_review(review_id):
    srp = sirope.Sirope()
    review = srp.find_first(ReviewDto, lambda r: str(r.get_oid()) == review_id)
    
    if not review or review.reviewer_email != UserDto.current_user().email:
        flask.flash("No tienes permiso para eliminar esta reseña.")
        return flask.redirect('/game/list')

    # Eliminar comentarios asociados a la reseña
    all_comments = list(srp.load_all(CommentDto))
    comments_to_delete = [comment for comment in all_comments if comment.review_id == review_id]
    for comment in comments_to_delete:
        srp.delete(comment.get_oid())
    
    # Eliminar la referencia a la reseña en el juego
    game = srp.find_first(GameDto, lambda g: g.get_id() == review.game_id)
    if game:
        try:
            game.reviews.remove(review.get_oid())
            srp.save(game)
        except ValueError:
            pass  # La reseña ya no estaba en la lista, no pasa nada.

    # Eliminar la reseña
    srp.delete(review.get_oid())

    return flask.redirect(f'/game/details/{review.game_id}')


@flask_login.login_required
@review_blprint.route('/list/<game_id>', methods=['GET'])
def list_reviews(game_id):
    srp = sirope.Sirope()
    all_reviews = list(srp.load_all(ReviewDto))
    reviews = [review for review in all_reviews if review.game_id == game_id]
    
    game = srp.find_first(GameDto, lambda g: g.get_id() == game_id)
    
    if not game:
        flask.flash("Juego no encontrado.")
        return flask.redirect('/game/list')
    
    return flask.render_template('list_reviews.html', usr=UserDto.current_user(), reviews=reviews, game=game)

@flask_login.login_required
@review_blprint.route('/details/<review_id>', methods=['GET'])
def review_details(review_id):
    srp = sirope.Sirope()
    review = srp.find_first(ReviewDto, lambda r: str(r.get_oid()) == review_id)
    
    if not review:
        flask.flash("Reseña no encontrada.")
        return flask.redirect('/game/list')

    # Buscar todos los comentarios asociados a la reseña
    comments = list(srp.load_all(CommentDto))
    review_comments = [comment for comment in comments if comment.review_id == review_id]

    return flask.render_template('review_details.html', usr=UserDto.current_user(), review=review, comments=review_comments)
