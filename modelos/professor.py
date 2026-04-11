from extensao import bd
from flask_login import UserMixin


#herança: professor é model do sqlalchemy e tambem um UserMixin
class Professor(bd.Model, UserMixin):
    __tablename__ = 'professores'
    id = bd.Column(bd.Integer, primary_key=True)
    nome = bd.Column(bd.String)
    email = bd.Column(bd.String, unique=True)
    senha = bd.Column(bd.String)
    nome_projeto = bd.Column(bd.String)

    def __repr__(self):
        return f"Professor('{self.nome}', '{self.email}')"

    @property
    def is_professor(self):
        return True

    def get_id(self):
        return f"prof_{self.id}"






