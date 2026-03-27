from extensao import bd
from extensao import login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    #aqui eu carrego o usuario pelo id por meio do flask login puxando lá do banco
    return Professor.query.get(int(user_id))

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





