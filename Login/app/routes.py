from flask import Blueprint, render_template, request, redirect, url_for, session
from app import mysql

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # Muestra directamente la página de login en lugar de redirigir
    return render_template('login.html')

@main.route('/inicio')
def inicio():
    # Si el usuario no está autenticado, redirige a la página de login
    if 'logged' not in session:
        return redirect(url_for('main.login'))
    return render_template('inicio.html')

@main.route('/register')
def register():
    # Muestra directamente la página de registro en lugar de redirigir
    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'usuario' in request.form and 'password' in request.form:
        __usuario = request.form['usuario'].strip()
        __password = request.form['password'].strip()

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuariospass WHERE username = %s AND pass = %s', (__usuario, __password,))
        account = cur.fetchone()

        if account:
            session['logged'] = True
            return redirect(url_for('main.inicio'))
        else:
            # Mostrar la página de login con un mensaje de error
            return render_template('login.html', error='Usuario o Contraseña Incorrecto')

    # Muestra directamente la página de login en lugar de redirigir
    return render_template('login.html')

@main.route('/create-register', methods=['GET', 'POST'])
def create_register():
    if request.method == 'POST' and 'usuario-register' in request.form and 'gmail-register' in request.form and 'password-register' in request.form:
        __usuario = request.form['usuario-register'].strip()
        __gmail = request.form['gmail-register'].strip()
        __password = request.form['password-register'].strip()

        if len(__password) < 8:
            # Mostrar la página de registro con un mensaje de error
            return render_template('register.html', error='La contraseña debe tener al menos 8 caracteres')

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuariospass WHERE username = %s OR gmail = %s', (__usuario, __gmail,))
        verify = cur.fetchone()

        if not verify:
            cur.execute('INSERT INTO usuariospass (username, gmail, pass) VALUES (%s, %s, %s)', (__usuario, __gmail, __password,))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('main.login'))
        else:
            cur.close()
            # Mostrar la página de registro con un mensaje de error
            return render_template('register.html', error='El usuario ya existe')

    # Muestra directamente la página de registro en lugar de redirigir
    return render_template('register.html')
