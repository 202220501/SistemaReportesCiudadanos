# modulos/comentarios.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from firebase_config import db  # Usa la conexión central [cite: 222, 326]
from datetime import datetime

# Definimos el Blueprint para integrarlo en el main.py central [cite: 218]
comentarios_bp = Blueprint('comentarios', __name__)

@comentarios_bp.route("/comentarios")
def index_comentarios():
    try:
        # Recupera comentarios desde la colección compartida en Firestore [cite: 174, 213]
        comentarios_ref = db.collection("comentarios").order_by("fecha", direction="DESCENDING").stream()
        comentarios = [doc.to_dict() for doc in comentarios_ref]
        return render_template("comentarios.html", comentarios=comentarios)
    except Exception as e:
        return f"Error al conectar con Firebase: {e}"

@comentarios_bp.route("/guardar_comentario", methods=["POST"])
def guardar():
    reporte_id = request.form.get("reporte_id")
    nombre = request.form.get("nombre")
    comentario = request.form.get("comentario")

    if not nombre or not comentario:
        return redirect(url_for('comentarios.index_comentarios'))

    # Estructura de datos NoSQL para reportes [cite: 174, 175]
    db.collection("comentarios").add({
        "reporteId": reporte_id,
        "nombre": nombre,
        "comentario": comentario,
        "fecha": datetime.now()
    })

    return redirect(url_for('comentarios.index_comentarios'))