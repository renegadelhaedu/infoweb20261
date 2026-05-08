from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from decorators import professor_required
import requests

from repository.professor_repository import Professor_repository

#faz login, lista alunos, adiciona aluno, remove aluno

professor_dao = Professor_repository()


#instanciei uma blueprint para que eu possa usar para criar rotas
bp_prof = Blueprint('professor', __name__, url_prefix='/professor')

@bp_prof.route('/login', methods=['POST'])
def fazer_login_professor():
    email_login = request.form.get('usuario')
    senha = request.form.get('senha')
    print('chegou')
    #objeto trazido do banco de dados (None se nao existe)
    professor = professor_dao.verificar_login(email_login, senha)
    print(professor)
    if professor:#verifica se esse objeto possui instância

        #função utilizada para colocar o objeto professor na sessao sob responsabilidade do login manager
        login_user(professor)

        return redirect(url_for('professor.mostrar_principal'))

    return render_template('login.html' , msg='usuário nao encontrado')
    #em sala mostrei as duas formas
    #return redirect(url_for('home_page'))

@bp_prof.route('/cadastrar', methods=['POST', 'GET'])
def cadastrar_professor():
    if request.method == 'GET':
        return render_template('cadastrarprofessor.html')

    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')
    nome_projeto = request.form.get('nome_projeto')

    #chama o repository para que seja inserido no banco de dados
    saida = professor_dao.cadastrar_professor(nome, email, senha, nome_projeto)
    if saida:
        return render_template('login.html')
    else:
        return render_template('login.html')#falta adicionar mensagem de erro


@bp_prof.route('/principal')
@login_required
@professor_required
def mostrar_principal():
    print('entrou no principal de professor')
    #aqui vc pode usar o current_user para pegar dados do usuario logado (objeto professor)
    print('usuario logado' , current_user.nome)
    return render_template('principalprofessor.html')



@bp_prof.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home_page'))


@bp_prof.route('/buzinar')
@login_required
def buzzer():
    url_esp32 = "http://192.168.3.3/acionar"

    try:
        resposta = requests.get(url_esp32, timeout=5)

        if resposta.status_code == 200:
            return "deu certo", 200
        else:
            return "deu ruim", 500

    except requests.exceptions.RequestException as e:
        return "a infeliz da ESP32 offline ou inacessível", 500


