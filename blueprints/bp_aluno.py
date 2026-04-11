from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required


from dao.aluno_dao import AlunoDao
from dao.professor_dao import ProfessorDao
aluno_dao = AlunoDao()
professor_dao = ProfessorDao()


bp_aluno = Blueprint('aluno', __name__, url_prefix='/aluno')

@bp_aluno.route('/login', methods=['POST'])
def fazer_login_professor():
    email_login = request.form.get('usuario')
    senha = request.form.get('senha')

    #objeto trazido do banco de dados (None se nao existe)
    aluno = aluno_dao.login_aluno(email_login, senha)

    if aluno:#verifica se esse objeto possui instância

        #função utilizada para colocar o objeto aluno na sessao sob responsabilidade do login manager
        login_user(aluno)

        return redirect(url_for('aluno.mostrar_principal'))

    return render_template('login.html',nome='wacelys', msg='usuário nao encontrado')
    #em sala mostrei as duas formas
    #return redirect(url_for('home_page'))

@bp_aluno.route('/cadastrar', methods=['POST', 'GET'])
def cadastrar_aluno():
    if request.method == 'GET':
        professores = professor_dao.listar_professores()
        #tem que fazer uma verificaçao se tem prof cadastrado. se nao tem, nao pode cadastrar aluno

        return render_template('cadastraraluno.html' , professores=professores)

    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')
    id_professor = request.form.get('id_professor')
    print(id_professor)
    #chama o dao para que seja inserido no banco de dados
    saida = aluno_dao.cadastrar_aluno(nome, email, senha, id_professor)
    if saida:
        return render_template('login.html')
    else:
        return render_template('login.html')#falta adicionar mensagem de erro


@bp_aluno.route('/principal')
@login_required
def mostrar_principal():
    #aqui vc pode usar o current_user para pegar dados do usuario logado
    return render_template('principalaluno.html')



@bp_aluno.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home_page'))
