# =====================================================
# MODULO HISTORIAL
# SISTEMA REPORTES CIUDADANOS
# =====================================================

from flask import Blueprint, render_template, request, redirect, url_for, flash
from firebase_admin import firestore

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
# MOSTRAR HISTORIAL
# =====================================================

@historial_bp.route('/historial')
def historial():

    lista_historial = []

    try:

        historial_db = db.collection(
            "historial"
        ).stream()

        for item in historial_db:

            datos = item.to_dict()

            lista_historial.append(
                datos
            )

    except Exception as e:

        print("Error:", e)

    return render_template(
        'historial.html',
        historial=lista_historial
    )

# =====================================================
# GUARDAR HISTORIAL
# =====================================================

@historial_bp.route(
    '/guardar_historial',
    methods=['POST']
)
def guardar_historial():

    try:

        reporte_id = request.form['reporte_id']

        usuario_id = request.form['usuario_id']

        estado_id = request.form['estado_id']

        tipo_evento = request.form['tipo_evento']

        descripcion_cambio = request.form[
            'descripcion_cambio'
        ]

        comentario = request.form[
            'comentario'
        ]

        if (
            reporte_id == "" or
            usuario_id == "" or
            estado_id == ""
        ):

            flash(
                "Completa todos los campos",
                "warning"
            )

            return redirect(
                url_for(
                    'historial.historial'
                )
            )

        datos = {

            "reporte_id": reporte_id,

            "usuario_id": usuario_id,

            "estado_id": estado_id,

            "tipo_evento": tipo_evento,

            "descripcion_cambio":
            descripcion_cambio,

            "comentario": comentario,

            "fecha_cambio":
            firestore.SERVER_TIMESTAMP

        }

        db.collection(
            "historial"
        ).add(datos)

        flash(
            "Historial guardado correctamente",
            "success"
        )

    except Exception as e:

        flash(
            str(e),
            "danger"
        )

    return redirect(
        url_for(
            'historial.historial'
        )
    )