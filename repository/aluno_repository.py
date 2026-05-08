#aqui a gente manipula objetos no banco. nao tem regra de negócio
from extensao import bd
from modelos.aluno import Aluno

class AlunoRepository:
    def buscar_por_email_e_senha(self, email, senha):
        return Aluno.query.filter_by(email=email, senha=senha).first()

    def salvar(self, aluno):
        try:
            bd.session.add(aluno)
            bd.session.commit()
            return True
        except Exception as e:
            print(f"Erro ao salvar aluno: {e}")
            bd.session.rollback()
            return False

    def listar_todos(self):
        return Aluno.query.all()