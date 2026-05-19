from firebase_config import db
# =====================================================
# MODULO HISTORIAL DE ESTADOS
# FLASK + FIREBASE
# =====================================================

from flask import Blueprint, render_template, request, redirect, url_for, flash
from firebase_admin import firestore
from datetime import datetime

# =====================================================
# BLUEPRINT
# =====================================================

historial_bp = Blueprint(
    'historial',
    __name__
)

# =====================================================
# FIREBASE
# =====================================================

db = firestore.client()

# =====================================================
# MOSTRAR PAGINA
# =====================================================

@historial_bp.route('/historial')
def historial():

    historial_datos = []

    return render_template(
        'historial.html',
        historial=historial_datos
    )

# =====================================================
# GUARDAR ESTADO
# =====================================================

@historial_bp.route('/guardar_estado', methods=['POST'])
def guardar_estado():

    try:

        id_reporte = request.form['id_reporte']
        estado = request.form['estado']
        usuario = request.form['usuario']
        comentario = request.form['comentario']

        if (
            id_reporte == "" or
            estado == "" or
            usuario == ""
        ):

            flash(
                "Completa todos los campos",
                "warning"
            )

            return redirect(
                url_for('historial.historial')
            )

        datos = {

            "estado": estado,
            "usuario": usuario,
            "comentario": comentario,
            "fecha": datetime.now().strftime(
                "%d/%m/%Y %H:%M:%S"
            )

        }

        db.collection("reportes") \
          .document(id_reporte) \
          .collection("historial_estados") \
          .add(datos)

        flash(
            "Estado guardado correctamente",
            "success"
        )

    except Exception as e:

        flash(str(e), "danger")

    return redirect(
        url_for('historial.ver_historial',
        id_reporte=id_reporte)
    )

# =====================================================
# MOSTRAR HISTORIAL
# =====================================================

@historial_bp.route('/ver_historial/<id_reporte>')
def ver_historial(id_reporte):

    historial_datos = []

    try:

        historial = db.collection("reportes") \
                      .document(id_reporte) \
                      .collection("historial_estados") \
                      .stream()

        for item in historial:

            historial_datos.append(
                item.to_dict()
            )

    except Exception as e:

        flash(str(e), "danger")

    return render_template(
        'historial.html',
        historial=historial_datos,
        id_reporte=id_reporte
    )