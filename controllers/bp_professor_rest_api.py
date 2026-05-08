from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from decorators import professor_required
from services.professor_service import ProfessorService
from services.aluno_service import AlunoService

bp_prof = Blueprint('professor', __name__, url_prefix='/api/professor')
professor_service = ProfessorService()
aluno_service = AlunoService()


@bp_prof.route('/login', methods=['POST'])
def api_fazer_login():
    #people, lembrem que tudo agora é: receber e devolver JSON
    dados = request.get_json()

    if not dados or 'usuario' not in dados or 'senha' not in dados:
        return jsonify({"erro": "Dados incompletos. Informe usuario e senha."}), 400

    email_login = dados.get('usuario')
    senha = dados.get('senha')

    professor = professor_service.autenticar_professor(email_login, senha)

    if professor:
        login_user(professor)

        return jsonify({
            "mensagem": "Login realizado com sucesso",
            "professor": {
                "id": professor.id,
                "nome": professor.nome
            }
        }), 200


    return jsonify({"erro": "Usuário ou senha inválidos"}), 401


@bp_prof.route('/cadastrar', methods=['POST'])
def api_cadastrar_professor():
    # agora nao tem mais GET para devolver a pag de cadastro
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Nenhum dado fornecido."}), 400

    nome = dados.get('nome')
    email = dados.get('email')
    senha = dados.get('senha')
    nome_projeto = dados.get('nome_projeto')

    professor_salvo = professor_service.cadastrar_professor(nome, email, senha, nome_projeto)

    if professor_salvo:
        # 201 (Created) q é o padrao REST para criar algo
        return jsonify({"mensagem": "Professor cadastrado com sucesso!"}), 201
    else:
        # Status 400 (Bad Request) ou 409 (Conflict)
        return jsonify({"erro": "Erro ao cadastrar professor. Verifique os dados."}), 400


@bp_prof.route('/perfil', methods=['GET'])
@login_required
@professor_required
def api_mostrar_perfil():
    # lembrem que nao tem mais rota '/principal'
    return jsonify({
        "id": current_user.id,
        "nome": current_user.nome,
        "email": current_user.email,
        "projeto": current_user.nome_projeto
    }), 200


@bp_prof.route("/logout", methods=['POST'])
@login_required
def api_logout():
    # aqui a gente muda no backend o estado da sessao (ou invalida o token)
    logout_user()
    return jsonify({"mensagem": "Logout realizado com sucesso"}), 200


@bp_prof.route('/buzinar', methods=['POST'])
@login_required
def api_buzzer():

    sucesso = professor_service.acionar_buzzer_iot()

    if sucesso:
        return jsonify({"status": "sucesso", "mensagem": "chamei a ESP32"}), 200
    else:

        return jsonify({"status": "erro", "mensagem": "A infeliz da ESP32 está offline ou inacessível"}), 503


@bp_prof.route('/alunos', methods=['GET'])
def api_listar_alunos():

    lista_alunos = aluno_service.listar_todos_para_api()
    return jsonify(lista_alunos), 200

@bp_prof.route('/alunos/<int:id>', methods=['GET'])
def detalhar_aluno(id):
    print(id)
    lista_alunos = aluno_service.listar_todos_para_api()
    return jsonify(lista_alunos), 200


@bp_prof.route('/alunos/projeto/<nome>', methods=['GET'])
def detalhar_projeto(nome):
    print(nome)
    lista_alunos = aluno_service.listar_todos_para_api()
    return jsonify(lista_alunos), 200


