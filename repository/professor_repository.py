#aqui a gente manipula objetos no banco. nao tem regra de negócio
from extensao import bd
from modelos.professor import Professor

class Professor_repository:
    def __init__(self):
        self.bd = bd

    def verificar_login(self, email_usuario, senha_usuario):
        return Professor.query.filter_by(email=email_usuario, senha=senha_usuario).first()

    def cadastrar_professor(self, professor):
        try:
            self.bd.session.add(professor)
            self.bd.session.commit()
            return True
        except Exception as e:
            print(e)
            self.bd.session.rollback()
            return False

    def listar_professores(self):
        return Professor.query.all()