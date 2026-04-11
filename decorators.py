from functools import wraps
from flask import abort, redirect, url_for
from flask_login import current_user, logout_user

#criando decorator
def professor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('home_page'))


        if not current_user.is_professor:
            #ai vc pode mostrar alguma mensagem via flash ou use texto,  exmeplo:
            #flash('Acesso negado. aqui é restrito para professores', 'error')
            logout_user()
            return redirect(url_for('home_page'))

        #galera, se chegar até aqui é pq é professor e passou nos dois testes anteriores
        return f(*args, **kwargs)

    return decorated_function