from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/usuarios")
def usuarios():
    return render_template("usuarios.html")

@app.route("/reportes")
def reportes():
    return render_template("reportes.html")

@app.route("/categorias")
def categorias():
    return render_template("categorias.html")

@app.route("/gps")
def gps():
    return render_template("gps.html")

@app.route("/imagenes")
def imagenes():
    return render_template("imagenes.html")

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

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/auditoria")
def auditoria():
    return render_template("auditoria.html")

app.run(debug=True)