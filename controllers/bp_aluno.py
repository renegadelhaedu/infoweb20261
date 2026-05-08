from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_user, login_required, logout_user
from services.aluno_service import AlunoService

bp_aluno = Blueprint('aluno', __name__, url_prefix='/aluno')
aluno_service = AlunoService()


@bp_aluno.route('/login', methods=['POST'])
def fazer_login_aluno():
    email = request.form.get('usuario')
    senha = request.form.get('senha')

    aluno = aluno_service.autenticar_aluno(email, senha)

    if aluno:
        login_user(aluno)
        return redirect(url_for('aluno.mostrar_principal'))

    return render_template('login.html', msg='Usuário não encontrado')


@bp_aluno.route('/cadastrar', methods=['POST', 'GET'])
def cadastrar_aluno():
    if request.method == 'GET':

        professores = aluno_service.obter_professores_disponiveis()

        if professores:
            return render_template('cadastraraluno.html', professores=professores)

        return render_template('login.html', msg='Não há professores cadastrados no sistema.')

    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')
    id_professor = request.form.get('id_professor')

    sucesso = aluno_service.cadastrar_aluno(nome, email, senha, id_professor)

    if sucesso:
        return render_template('login.html', msg='Cadastro de aluno realizado!')

    return render_template('login.html', msg='Erro ao cadastrar aluno.')


@bp_aluno.route('/principal')
@login_required
def mostrar_principal():
    return render_template('principalaluno.html')

@bp_aluno.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home_page'))