from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from decorators import professor_required
from services.professor_service import ProfessorService
from services.aluno_service import AlunoService

bp_prof = Blueprint('professor', __name__, url_prefix='/professor')
professor_service = ProfessorService()
aluno_service = AlunoService()


@bp_prof.route('/login', methods=['POST'])
def fazer_login_professor():

    email_login = request.form.get('usuario')
    senha = request.form.get('senha')

    professor = professor_service.autenticar_professor(email_login, senha)

    if professor:
        #controle de acesso via sessão
        login_user(professor)
        return redirect(url_for('professor.mostrar_principal'))

    return render_template('login.html', msg='Usuário não encontrado')


@bp_prof.route('/cadastrar', methods=['POST', 'GET'])
def cadastrar_professor():
    if request.method == 'GET':
        return render_template('cadastrarprofessor.html')

    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')
    nome_projeto = request.form.get('nome_projeto')

    professor_salvo = professor_service.cadastrar_professor(nome, email, senha, nome_projeto)

    if professor_salvo:
        return render_template('login.html', msg='Cadastro realizado com sucesso!')
    else:
        return render_template('login.html', msg='Erro ao cadastrar.')


@bp_prof.route('/principal')
@login_required
@professor_required
def mostrar_principal():
    return render_template('principalprofessor.html')


@bp_prof.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home_page'))


@bp_prof.route('/buzinar')
@login_required
def buzzer():
    # O Controller não precisa saber o IP da placa ou a biblioteca requests
    sucesso = professor_service.acionar_buzzer_iot()

    if sucesso:
        return "deu certo", 200
    else:
        return "a infeliz da ESP32 offline ou inacessível", 500


@bp_prof.route('/listaralunos', methods=['GET'])
@login_required
@professor_required
def api_listar_alunos():
    lista_alunos = aluno_service.listar_todos_para_api()


    return jsonify(lista_alunos), 200