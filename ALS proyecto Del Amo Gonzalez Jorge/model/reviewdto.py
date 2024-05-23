import sirope

class ReviewDto:
    def __init__(self, game_id, reviewer_email, rating, comment):
        self.game_id = game_id
        self.reviewer_email = reviewer_email
        self.rating = rating
        self.comment = comment
        self.comments = []  # Lista para almacenar los OID de los comentarios
        self.__oid__ = None

    def get_id(self):
        return str(hash(f"{self.game_id}{self.reviewer_email}"))

    def get_oid(self):
        if self.__oid__ is None:
            self.__oid__ = sirope.OID(self.__class__.__name__, self.get_id())
        return self.__oid__
