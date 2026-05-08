import requests
from repository.professor_repository import Professor_repository
from modelos.professor import Professor


class ProfessorService:
    def __init__(self):
        self.repository = Professor_repository()

    def autenticar_professor(self, email, senha):
        #criei esta regra só p gerar exemplo
        if len(senha) <= 2 or len(email) < 5:
            return False
        return self.repository.verificar_login(email, senha)

    def cadastrar_professor(self, nome, email, senha, nome_projeto):
        #aqui a gente coloca regras se tiver (sei la, um hash de senha)
        if not email.endswith('@catolica.edu.br'):
            return False

        novo_professor = Professor(
            nome=nome,
            email=email,
            senha=senha,
            nome_projeto=nome_projeto
        )
        return self.repository.cadastrar_professor(novo_professor)

    def acionar_buzzer_iot(self):
        url_esp32 = "http://192.168.0.3/acionar"
        try:
            resposta = requests.get(url_esp32, timeout=5)
            return resposta.status_code == 200
        except requests.exceptions.RequestException:
            return False