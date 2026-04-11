from extensao import bd
from flask_login import UserMixin



class Aluno(bd.Model, UserMixin):
    __tablename__ = 'alunos'
    id = bd.Column(bd.Integer, primary_key=True)
    nome = bd.Column(bd.String)
    email = bd.Column(bd.String, unique=True)
    senha = bd.Column(bd.String)
    id_professor = bd.Column(bd.Integer)

    def __repr__(self):
        return f'<Nome: {self.nome}, Email: {self.email}, id: {self.id}>'

    @property
    def is_professor(self):
        return False

    #sobrecarregar este método de usermixin para informar ao login manager que tipo de usuário está logado
    def get_id(self):
        return f"aluno_{self.id}"



