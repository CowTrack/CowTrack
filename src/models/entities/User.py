from werkzeug.security import check_password_hash
from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, id, correo, password, nombre="") -> None:
        self.id = id
        self.nombre = nombre
        self.password = password
        self.correo = correo

    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)