from project import db
from project import bcrypt

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        super(Usuario, self).__init__(**kwargs)
        self.password = self.generate_password(**kwargs)

    def generate_password(self, **kwargs):
        if 'password' not in kwargs:
            return None
        return bcrypt.generate_password_hash(kwargs.get('password')).decode()
