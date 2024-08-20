from flask import render_template
from . import auth_bp

@auth_bp.route("/logear")
def logear():
    return render_template("auth/sesion.html")

@auth_bp.route("/register")
def register():
    return render_template("auth/registro.html")