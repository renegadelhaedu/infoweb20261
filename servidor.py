#no terminal => pip install flask
from flask import *
from blueprints.bp_professor import  bp_prof
from blueprints.bp_aluno import  bp_aluno
from extensao import bd
#esse login_manager é o objeto que controla os acessos
from extensao import login_manager
import os
from dotenv import load_dotenv

load_dotenv()

def criar_servidor():
    #instanciando o servidor web flask
    app = Flask(__name__)
    #gerar chave secreta para ser usado no controle de sessao(cookies)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_ECHO'] = True
    bd.init_app(app)

    #vinculando o login manager ao teu servidor flask
    login_manager.init_app(app)
    login_manager.login_view = 'home_page'

    #vinculando cada blueprint com o servidor flask
    app.register_blueprint(bp_prof)
    app.register_blueprint(bp_aluno)


    #criando uma rota (endpoint) de acesso no backend
    @app.route('/')
    def home_page():
        return render_template("login.html", nome='teste')

    #retornando o objeto que representa o servidor flask
    return app


if __name__ == '__main__':
    servidor = criar_servidor()
    with servidor.app_context():
        bd.create_all()
    #executa a aplicação web - servidor on
    servidor.run(debug=True, port=5000)

