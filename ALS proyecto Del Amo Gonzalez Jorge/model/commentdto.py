import sirope

class CommentDto:
    def __init__(self, review_id, commenter_email, comment):
        self.review_id = review_id
        self.commenter_email = commenter_email
        self.comment = comment
        self.__oid__ = None

    def get_id(self):
        return str(hash(f"{self.review_id}{self.commenter_email}{self.comment}"))

    def get_oid(self):
        if self.__oid__ is None:
            self.__oid__ = sirope.OID(self.__class__.__name__, self.get_id())
        return self.__oid__
