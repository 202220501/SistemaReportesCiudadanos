from flask import Blueprint, render_template, request, redirect, session
from firebase_config import db

usuarios_bp = Blueprint("usuarios", __name__)

# =========================
# REGISTRO
# =========================
@usuarios_bp.route("/registro", methods=["GET", "POST"])
def registro():

    if request.method == "POST":

        nombre = request.form["nombre"]
        correo = request.form["correo"]
        password = request.form["password"]

        db.collection("usuarios").add({
            "nombre": nombre,
            "correo": correo,
            "password": password
        })

        return redirect("/login")

    return render_template("registro.html")


# =========================
# LOGIN
# =========================
@usuarios_bp.route("/login", methods=["GET", "POST"])
def login():

    mensaje = ""

    if request.method == "POST":

        correo = request.form["correo"]
        password = request.form["password"]

        usuarios = db.collection("usuarios").stream()

        for usuario in usuarios:

            datos = usuario.to_dict()

            if datos["correo"] == correo and datos["password"] == password:

                session["usuario"] = datos["nombre"]

                return redirect("/usuarios")

        mensaje = "Correo o contraseña incorrectos"

    return render_template("login.html", mensaje=mensaje)


# =========================
# MOSTRAR USUARIOS
# =========================
@usuarios_bp.route("/usuarios")
def usuarios():

    if "usuario" not in session:
        return redirect("/login")

    lista_usuarios = []

    usuarios = db.collection("usuarios").stream()

    for usuario in usuarios:

        datos = usuario.to_dict()
        lista_usuarios.append(datos)

    return render_template(
        "usuarios.html",
        usuarios=lista_usuarios,
        nombre=session["usuario"]
    )


# =========================
# CERRAR SESION
# =========================
@usuarios_bp.route("/logout")
def logout():

    session.clear()

    return redirect("/login")