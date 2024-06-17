from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import mysql
import re

main = Blueprint('main', __name__)

def verify_data(nombre, apellido, correo, telefono):
    if not nombre.strip() or not apellido.strip():
        flash('Nombre y apellido necesarios', 'error')
        return False
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
        flash('Correo electrónico no es válido', 'error')
        return False
    elif not telefono.strip() or not telefono.isdigit() or len(telefono) < 7:
        flash('Número de teléfono no es válido', 'error')
        return False
    return True

@main.route('/')
def index():
    try:
        with mysql.connection.cursor() as cur:
            cur.execute('SELECT * FROM usuarios')
            data = cur.fetchall()
        return render_template('crud.html', usuarios=data)
    except Exception as e:
        flash(f'Error en la base de datos: {e}', 'error')
        return redirect(url_for('main.index'))

@main.route('/add_user', methods=['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        nombre = request.form['nombre'].strip().lower()
        apellido = request.form['apellido'].strip().lower()
        telefono = request.form['telefono']
        correo = request.form['correo']
        fecha = request.form['fecha']
        genero = request.form['genero']
        
        if not verify_data(nombre, apellido, correo, telefono):
            return redirect(url_for('main.index'))

        try:
            with mysql.connection.cursor() as cur:
                cur.execute('SELECT * FROM usuarios WHERE nombre = %s AND apellido = %s', (nombre, apellido))
                data = cur.fetchall()
                if not data:
                    cur.execute('INSERT INTO usuarios (nombre, apellido, telefono, correo, fecha, genero) VALUES (%s, %s, %s, %s, %s, %s)', (nombre, apellido, telefono, correo, fecha, genero))
                    mysql.connection.commit()
                    flash('Usuario agregado correctamente', 'success')
                else:
                    flash(f'El usuario {nombre} {apellido} ya existe', 'error')
        except Exception as e:
            flash(f'Error: {e}', 'error')
        return redirect(url_for('main.index'))

@main.route('/edit_user/<string:id>')
def edit_user(id):
    try:
        with mysql.connection.cursor() as cur:
            cur.execute('SELECT * FROM usuarios WHERE id= %s',(id,))
            data= cur.fetchall()
            return render_template('update.html', usuarios= data[0])
    except Exception as e:
        flash(f'Error {e}')
        return 'Error'
    finally:
        cur.close()

@main.route('/update_user/<string:id>', methods= ['POST'])
def update_user(id):
    nombre= request.form['nombre'].strip().lower()
    apellido= request.form['apellido'].strip().lower()
    telefono= request.form['telefono']
    correo= request.form['correo']
    fecha= request.form['fecha']
    genero= request.form['genero']
    
    verify_data(nombre, apellido, correo, telefono)
    
    try:
        with mysql.connection.cursor() as cur:
            cur.execute('UPDATE usuarios SET nombre= %s, apellido= %s, telefono= %s, correo= %s, fecha= %s, genero= %s WHERE id= %s',(nombre, apellido, telefono, correo, fecha, genero, id))
            mysql.connection.commit()
            flash('Usuario actualizado correctamente', 'success')
            return redirect(url_for('main.index'))
    except mysql.Error as a:
        flash(f'Error en la base de datos {a}', 'error')
    except Exception as e:
        flash(f'Error {e}', 'error')
    finally:
        cur.close()
        
@main.route('/delete/<string:id>')
def delete(id):
    try:
        with mysql.connection.cursor() as cur:
            cur.execute('DELETE FROM usuarios WHERE id = {0}'.format(id))
            mysql.connection.commit()
            return redirect(url_for('main.index'))
    except mysql.Error as a:
        flash(f'Error en la base de datos {a}', 'error')
    except Exception as e:
        flash(f'Error {e}', 'error')
    finally:
        cur.close()

@main.route('/order/<string:id>')
def order(id):
    direction = request.args.get('direction', 'asc')
    if direction == 'asc':
        order_by = 'ASC'
        next_direction = 'desc'
    else:
        order_by = 'DESC'
        next_direction = 'asc'
        
    try:
        with mysql.connection.cursor() as cur:
            cur.execute(f'SELECT * FROM usuarios ORDER BY {id} {order_by}')
            data = cur.fetchall()
            return render_template('crud.html', usuarios=data, next_direction=next_direction)
    except mysql.Error as a:
        flash(f'Error en la base de datos {a}', 'error')
    except Exception as e:
        flash(f'Error {e}', 'error')
    finally:
        cur.close()