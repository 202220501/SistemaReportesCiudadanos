# =========================================
# MODULO ESTADOS
# =========================================

from flask import Blueprint, render_template, request
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

    buscar = request.args.get(
        "buscar",
        ""
    ).lower()

    estado_filtro = request.args.get(
        "estado",
        "Todos"
    )

    categoria_filtro = request.args.get(
        "categoria",
        "Todas"
    )

    try:

        reportes_db = db.collection(
            "reportes"
        ).stream()

        for reporte in reportes_db:

            datos = reporte.to_dict()

            datos["id"] = reporte.id

            titulo = datos.get(
                "titulo",
                ""
            ).lower()

            categoria = str(
                datos.get(
                    "categoria_id",
                    ""
                )
            )

            # =========================================
            # BUSQUEDA
            # =========================================

            if buscar != "":

                if buscar not in titulo:
                    continue

            estado_id = datos.get(
                "estado_id",
                "1"
            )

            # =========================================
            # ESTADOS
            # =========================================

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

            # =========================================
            # ASIGNACION
            # =========================================

            datos["dependencia_asignada"] = datos.get(
                "dependencia_asignada",
                "Sin asignar"
            )

            datos["estado_asignacion"] = datos.get(
                "estado_asignacion",
                "Pendiente"
            )

            # =========================================
            # FILTRO ESTADO
            # =========================================

            if estado_filtro != "Todos":

                if datos["estado"] != estado_filtro:
                    continue

            # =========================================
            # FILTRO CATEGORIA
            # =========================================

            if categoria_filtro != "Todas":

                if categoria != categoria_filtro:
                    continue

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