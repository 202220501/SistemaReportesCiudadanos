# =====================================================
# MODULO REPORTES
# FLASK + FIREBASE
# =====================================================

from flask import Blueprint, render_template, request, redirect, url_for, flash
from firebase_admin import firestore
from datetime import datetime

# =====================================================
# BLUEPRINT
# =====================================================

reportes_bp = Blueprint(
    'reportes',
    _name_
)

# =====================================================
# FIREBASE
# =====================================================

db = firestore.client()

# =====================================================
# MOSTRAR PAGINA
# =====================================================

@reportes_bp.route('/reportes')
def reportes():

    lista_reportes = []

    try:

        reportes_db = db.collection(
            "reportes"
        ).stream()

        for reporte in reportes_db:

            datos = reporte.to_dict()

            lista_reportes.append(datos)

    except Exception as e:

        print(e)

    return render_template(
        'reportes.html',
        reportes=lista_reportes
    )

# =====================================================
# ENVIAR REPORTE
# =====================================================

@reportes_bp.route(
    '/enviar_reporte',
    methods=['POST']
)
def enviar_reporte():

    try:

        nombre = request.form['nombre']
        correo = request.form['correo']
        tipo = request.form['tipo']
        descripcion = request.form['descripcion']
        ubicacion = request.form['ubicacion']
        prioridad = request.form['prioridad']

        if (
            nombre == "" or
            correo == "" or
            descripcion.strip() == ""
        ):

            flash(
                "Completa todos los campos",
                "warning"
            )

            return redirect(
                url_for('reportes.reportes')
            )

        reporte = {

            "nombre": nombre,
            "correo": correo,
            "tipo_reporte": tipo,
            "descripcion": descripcion,
            "ubicacion": ubicacion,
            "prioridad": prioridad,
            "estado": "Pendiente",
            "fecha": datetime.now().strftime(
                "%d/%m/%Y %H:%M:%S"
            )

        }

        db.collection(
            "reportes"
        ).add(reporte)

        flash(
            "Reporte enviado correctamente",
            "success"
        )

    except Exception as e:

        flash(str(e), "danger")

    return redirect(
        url_for('reportes.reportes')
    )