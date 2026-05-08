from repository.aluno_repository import AlunoRepository
from repository.professor_repository import Professor_repository
from modelos.aluno import Aluno

class AlunoService:
    def __init__(self):
        self.aluno_repo = AlunoRepository()
        self.prof_repo = Professor_repository()

    def autenticar_aluno(self, email, senha):
        return self.aluno_repo.buscar_por_email_e_senha(email, senha)

    def obter_professores_disponiveis(self):
        #vamos botar uma regra de aluno só pode ser cadastrado se houver professor
        return self.prof_repo.listar_professores()

    def cadastrar_aluno(self, nome, email, senha, id_professor):
        #galera, se quiserem, usem validações aqui (id professor valido, etc)
        novo_aluno = Aluno(
            nome=nome,
            email=email,
            senha=senha,
            id_professor=id_professor
        )
        return self.aluno_repo.salvar(novo_aluno)

    def listar_todos_para_api(self):
        alunos = self.aluno_repo.listar_todos()
        #seria bom a gente aqui retirar as senhas
        return [aluno.to_dict() for aluno in alunos]