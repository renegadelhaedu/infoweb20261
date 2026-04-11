from extensao import bd
from modelos.aluno import Aluno

class AlunoDao:
    def __init__(self):
        self.bd = bd

    def login_aluno(self, email_usuario, senha_usuario):
        return Aluno.query.filter_by(email=email_usuario, senha=senha_usuario).first()

    def cadastrar_aluno(self, nome, email, senha, id_professor):
        aluno = Aluno(nome=nome, email=email, senha=senha, id_professor=id_professor)
        try:
            self.bd.session.add(aluno)
            self.bd.session.commit()
            return True
        except Exception as e:
            print(e)
            self.bd.session.rollback()
            return False