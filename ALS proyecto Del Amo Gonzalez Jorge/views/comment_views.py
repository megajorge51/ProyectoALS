import flask
import flask_login
import sirope
from model.commentdto import CommentDto
from model.reviewdto import ReviewDto
from model.userdto import UserDto

comment_blprint = flask.Blueprint('comment', __name__, url_prefix='/comment')

@flask_login.login_required
@comment_blprint.route('/add/<review_id>', methods=['POST'])
def add_comment(review_id):
    srp = sirope.Sirope()
    user = UserDto.current_user()
    comment_text = flask.request.form.get('comment')

    if not comment_text.strip():
        flask.flash("El comentario no puede estar vacío.")
        return flask.redirect(flask.url_for('review.review_details', review_id=review_id))

    comment = CommentDto(review_id, user.email, comment_text)
    srp.save(comment)

    review = srp.find_first(ReviewDto, lambda r: str(r.get_oid()) == review_id)
    if review:
        review.comments.append(comment.get_oid())
        srp.save(review)
    else:
        flask.flash("Reseña no encontrada.")
        return flask.redirect('/game/list')

    return flask.redirect(flask.url_for('review.review_details', review_id=review_id))

@flask_login.login_required
@comment_blprint.route('/delete/<comment_id>', methods=['POST'])
def delete_comment(comment_id):
    srp = sirope.Sirope()
    user = UserDto.current_user()

    comment = srp.find_first(CommentDto, lambda c: str(c.get_oid()) == comment_id)
    if comment and comment.commenter_email == user.email:
        review = srp.find_first(ReviewDto, lambda r: r.get_oid() == comment.review_id)
        if review:
            review.comments.remove(comment.get_oid())
            srp.save(review)
        srp.delete(comment.get_oid())  # Utilizar remove en lugar de delete
        flask.flash("Comentario eliminado.")
    else:
        flask.flash("No tienes permiso para eliminar este comentario.")

    return flask.redirect(flask.url_for('review.review_details', review_id=comment.review_id))
