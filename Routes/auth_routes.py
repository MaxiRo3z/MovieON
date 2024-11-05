from flask import render_template, request, redirect, url_for, flash, session
from . import auth_bp
from werkzeug.security import generate_password_hash, check_password_hash
from database.models import User
from database.db import session  as db_session# Importa la sesión desde db.py
from sqlalchemy.exc import IntegrityError

@auth_bp.route("/logear", methods=['GET', 'POST'])
def logear():
    if request.method == 'POST':
        username= request.form['username']
        password= request.form['password']

        user = db_session.query(User).filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash,password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('main.index'))
        flash('Nombre de usuario o contraseña incorrectos', 'danger')
    
    return render_template("auth/sesion.html")

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('main.index'))

@auth_bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['full_name']  # Nuevo
        username = request.form['username']
        email = request.form['email']  # Nuevo
        password = request.form['password']
        password_hash = generate_password_hash(password, method='pbkdf2:sha256')

        try:
            existing_user = db_session.query(User).filter((User.username == username) | (User.email == email)).first()
            if existing_user:
                flash('El nombre de usuario o correo ya está en uso')
                return redirect(url_for('auth.register'))

            new_user = User(username=username, password_hash=password_hash, email=email, full_name=full_name)  # Actualizado
            db_session.add(new_user)
            db_session.commit()
            flash('Registro exitoso!')
            return redirect(url_for('auth.logear'))
        except IntegrityError:
            db_session.rollback()
            flash('Error al registrar el usuario.')
        except Exception as e:
            db_session.rollback()
            flash(f'Error inesperado: {e}')

    return render_template("auth/registro.html")