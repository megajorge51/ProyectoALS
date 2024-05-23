import sirope

class GameDto:
    def __init__(self, title, description, developer, genre, platform, owner_email):
        self.title = title
        self.description = description
        self.developer = developer
        self.genre = genre
        self.platform = platform
        self.owner_email = owner_email
        self.reviews = []  # Lista para almacenar los OID de las reseñas
        self.__oid__ = None

    def get_id(self):
        return str(hash(f"{self.title}{self.owner_email}"))

    def get_oid(self):
        if self.__oid__ is None:
            self.__oid__ = sirope.OID(self.__class__.__name__, self.get_id())
        return self.__oid__
