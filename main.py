from flask import Flask, render_template, request
from firebase_config import db

# =====================================
# IMPORTAR MODULOS
# =====================================

from modulos.usuarios import usuarios_bp
from modulos.historial import historial_bp
from modulos.reportes import reportes_bp
from modulos.imagenes import (imagenes_bp, procesar_imagenes)
from modulos.categorias import categorias_bp
from modulos.auditoria import auditoria_bp

# =====================================
# APP
# =====================================



app = Flask(__name__)

# =====================================
# CLAVE DE SESION
# =====================================

app.secret_key = "123456"

# =====================================
# REGISTRAR MODULOS
# =====================================

app.register_blueprint(usuarios_bp)
app.register_blueprint(reportes_bp)
app.register_blueprint(categorias_bp)
app.register_blueprint(imagenes_bp)
app.register_blueprint(historial_bp)
app.register_blueprint(auditoria_bp)


# =====================================
# RUTAS
# =====================================
# ==========================================
# IMPORTAR MODULOS
# ==========================================

from modulos.usuarios import usuarios_bp
from modulos.auditoria import auditoria_bp

# 1. IMPORTAMOS TU MÓDULO AQUÍ
from modulos.admin import admin_bp

# ==========================================
# APP
# ==========================================

app = Flask(__name__)

# ==========================================
# CLAVE DE SESION
# ==========================================

app.secret_key = "123456"

# ==========================================
# REGISTRAR MODULOS
# ==========================================

app.register_blueprint(usuarios_bp)
app.register_blueprint(auditoria_bp)

# 2. REGISTRAMOS TU MÓDULO AQUÍ
app.register_blueprint(admin_bp)

# ==========================================
# RUTAS
# ==========================================


@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/usuarios")
def usuarios():
    return render_template("usuarios.html")

@app.route("/categorias")
def categorias():
    return render_template("categorias.html")
@app.route("/reportes")
def reportes():
    return render_template("reportes.html")

# =====================================
# CATEGORIAS
# =====================================

# ESTA RUTA SE ELIMINA
# PORQUE categorias.py YA LA CONTROLA

# @app.route("/categorias")
# def categorias():
#     return render_template("categorias.html")

@app.route("/gps")
def gps():
    return render_template("gps.html")

# =====================================
# IMAGENES
# =====================================

@app.route(
    "/imagenes",
    methods=["GET", "POST"]
)
def imagenes():

    if request.method == "POST":
        return procesar_imagenes()

    return render_template(
        "imagenes.html"
    )

@app.route("/estados")
def estados():
    return render_template("estados.html")

@app.route("/historial")
def historial():
    return render_template("historial.html")

@app.route("/comentarios")
def comentarios():
    return render_template("comentarios.html")

@app.route("/votos")
def votos():
    return render_template("votos.html")

@app.route("/dependencias")
def dependencias():
    return render_template("dependencias.html")

@app.route("/asignaciones")
def asignaciones():
    return render_template("asignaciones.html")

# 3. SILENCIAMOS ESTA RUTA PARA QUE NO CHOQUE CON LA TUYA
# @app.route("/admin")
# def admin():
#     return render_template("admin.html")

@app.route("/gestiondisp")
def gestiondisp():
    return render_template("gestiondisp.html")

# =====================================
# EJECUTAR
# =====================================

if __name__ == "__main__":

    app.run(debug=True)
# ==========================================
# EJECUTAR
# ==========================================

app.run(debug=True)