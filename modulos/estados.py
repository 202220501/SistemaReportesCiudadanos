# =========================================
# MODULO ESTADOS
# =========================================

from flask import Blueprint, render_template, redirect
from firebase_config import db

# =========================================
# BLUEPRINT
# =========================================

estados_bp = Blueprint(
    "estados",
    __name__
)

# =========================================
# MOSTRAR ESTADOS
# =========================================

@estados_bp.route("/estados")
def estados():

    lista_reportes = []

    pendientes = 0
    proceso = 0
    resueltos = 0
    cancelados = 0

    try:

        reportes_db = db.collection(
            "reportes"
        ).stream()

        for reporte in reportes_db:

            datos = reporte.to_dict()

            datos["id"] = reporte.id

            estado_id = datos.get(
                "estado_id",
                "1"
            )

            # =========================
            # ESTADOS
            # =========================

            if estado_id == "1":

                datos["estado"] = "Pendiente"
                datos["clase_estado"] = "pendiente"

                pendientes += 1

            elif estado_id == "2":

                datos["estado"] = "En proceso"
                datos["clase_estado"] = "proceso"

                proceso += 1

            elif estado_id == "3":

                datos["estado"] = "Resuelto"
                datos["clase_estado"] = "resuelto"

                resueltos += 1

            elif estado_id == "4":

                datos["estado"] = "Cancelado"
                datos["clase_estado"] = "cancelado"

                cancelados += 1

            else:

                datos["estado"] = "Desconocido"
                datos["clase_estado"] = "secondary"

            lista_reportes.append(
                datos
            )

    except Exception as e:

        print(e)

    return render_template(

        "estados.html",

        reportes=lista_reportes,

        pendientes=pendientes,
        proceso=proceso,
        resueltos=resueltos,
        cancelados=cancelados

    )

# =========================================
# VER REPORTE
# =========================================

@estados_bp.route("/ver_reporte/<id>")
def ver_reporte(id):

    try:

        reporte_ref = db.collection(
            "reportes"
        ).document(id)

        reporte = reporte_ref.get()

        if reporte.exists:

            datos = reporte.to_dict()
            datos["id"] = reporte.id

            return render_template(
                "detalle_reporte.html",
                reporte=datos
            )

        return "Reporte no encontrado"

    except Exception as e:

        return str(e)

# =========================================
# ACTUALIZAR ESTADO
# =========================================

@estados_bp.route("/actualizar_estado/<id>")
def actualizar_estado(id):

    try:

        reporte_ref = db.collection(
            "reportes"
        ).document(id)

        reporte = reporte_ref.get()

        if reporte.exists:

            datos = reporte.to_dict()

            estado_actual = datos.get(
                "estado_id",
                "1"
            )

            nuevo_estado = "1"

            if estado_actual == "1":
                nuevo_estado = "2"

            elif estado_actual == "2":
                nuevo_estado = "3"

            elif estado_actual == "3":
                nuevo_estado = "4"

            reporte_ref.update({

                "estado_id": nuevo_estado

            })

        return redirect("/estados")

    except Exception as e:

        return str(e)