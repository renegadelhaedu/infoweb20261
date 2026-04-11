from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

#instanciar o objeto do login manager
login_manager = LoginManager()
bd = SQLAlchemy()

#ensinar para o login manager como carrega usuários de acordo com o tipo
@login_manager.user_loader
def load_user(user_id):
    #coloquei aqui dentro p evitar import circular
    from modelos.professor import Professor
    from modelos.aluno import Aluno

    try:
        tipo_usuario, id_numerico = user_id.split('_')
        id_numerico = int(id_numerico)

        if tipo_usuario == 'prof':
            return Professor.query.get(id_numerico)
        elif tipo_usuario == 'aluno':
            return Aluno.query.get(id_numerico)

    except ValueError:
        return None

    return None