from firebase_config import db
from flask import Blueprint, render_template, request, redirect, flash

asignaciones_bp = Blueprint(
    'asignaciones',
    __name__
)

# =====================================
# MOSTRAR REPORTES Y DEPENDENCIAS
# =====================================

@asignaciones_bp.route('/asignaciones')
def asignaciones():

    lista_reportes = []
    lista_dependencias = []

    # =====================================
    # OBTENER REPORTES
    # =====================================

    reportes_db = db.collection(
        'reportes'
    ).stream()

    for reporte in reportes_db:

        datos = reporte.to_dict()

        datos['id_reporte'] = reporte.id

        lista_reportes.append(
            datos
        )

    # =====================================
    # OBTENER DEPENDENCIAS
    # =====================================

    dependencias_db = db.collection(
        'dependencias'
    ).stream()

    for dependencia in dependencias_db:

        dep = dependencia.to_dict()

        dep['id_dependencia'] = dependencia.id

        lista_dependencias.append(
            dep
        )

    return render_template(

        'asignaciones.html',

        reportes=lista_reportes,
        dependencias=lista_dependencias

    )

# =====================================
# ASIGNAR REPORTE
# =====================================

@asignaciones_bp.route(
    '/asignar_reporte/<id>',
    methods=['POST']
)
def asignar_reporte(id):

    dependencia = request.form['dependencia']

    try:

        db.collection(
            'reportes'
        ).document(id).update({

            'dependencia_asignada': dependencia,
            'estado_asignacion': 'Asignado'

        })

        flash(
            "Reporte asignado correctamente ✅",
            "success"
        )

    except Exception as e:

        print(e)

        flash(
            "Error al asignar reporte ❌",
            "danger"
        )

    return redirect('/asignaciones')