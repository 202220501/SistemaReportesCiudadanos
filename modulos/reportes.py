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
    __name__
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

        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        categoria_id = request.form['categoria_id']
        usuario_id = request.form['usuario_id']
        prioridad = request.form['prioridad']
        direccion = request.form['direccion']
        latitud = request.form['latitud']
        longitud = request.form['longitud']
        imagen = request.form['imagen']

        if (
            titulo.strip() == "" or
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

            "titulo": titulo,
            "descripcion": descripcion,
            "categoria_id": categoria_id,
            "usuario_id": usuario_id,
            "estado_id": "1",
            "latitud": latitud,
            "longitud": longitud,
            "direccion": direccion,
            "fecha_reporte": datetime.now().strftime(
                "%d/%m/%Y %H:%M:%S"
            ),
            "imagen": imagen,
            "prioridad": prioridad

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