# =========================================
# MODULO GESTION DISPOSITIVOS
# =========================================

from flask import Blueprint, render_template, request, redirect
from firebase_config import db

# =========================================
# BLUEPRINT
# =========================================

gestiondisp_bp = Blueprint(
    "gestiondisp",
    __name__
)

# =========================================
# MOSTRAR DISPOSITIVOS
# =========================================

@gestiondisp_bp.route("/gestiondisp")
def gestiondisp():

    lista_dispositivos = []

    activos = 0
    inactivos = 0
    celulares = 0
    usuarios = 0

    buscar = request.args.get(
        "buscar",
        ""
    ).lower()

    try:

        dispositivos_db = db.collection(
            "dispositivos"
        ).stream()

        for dispositivo in dispositivos_db:

            datos = dispositivo.to_dict()

            datos["id"] = dispositivo.id

            nombre = datos.get(
                "nombre",
                ""
            ).lower()

            dispositivo_nombre = datos.get(
                "dispositivo",
                ""
            ).lower()

            # =========================================
            # FILTRO BUSQUEDA
            # =========================================

            if buscar != "":

                if buscar not in nombre and buscar not in dispositivo_nombre:
                    continue

            usuarios += 1

            # =========================================
            # ESTADO
            # =========================================

            estado = datos.get(
                "estado",
                "Activo"
            )

            if estado == "Activo":

                activos += 1
                datos["clase_estado"] = "activo"

            else:

                inactivos += 1
                datos["clase_estado"] = "inactivo"

            # =========================================
            # CELULARES
            # =========================================

            dispositivo_texto = datos.get(
                "dispositivo",
                ""
            ).lower()

            if "iphone" in dispositivo_texto or "samsung" in dispositivo_texto or "xiaomi" in dispositivo_texto:

                celulares += 1

            lista_dispositivos.append(
                datos
            )

    except Exception as e:

        print(e)

    return render_template(

    "gestiondisp.html",

        dispositivos=lista_dispositivos,

        usuarios=usuarios,
        activos=activos,
        celulares=celulares,
        inactivos=inactivos

    )

# =========================================
# AGREGAR DISPOSITIVO
# =========================================

@gestiondisp_bp.route(
    "/agregar_dispositivo",
    methods=["POST"]
)
def agregar_dispositivo():

    try:

        nombre = request.form["nombre"]

        correo = request.form["correo"]

        dispositivo = request.form["dispositivo"]

        sistema = request.form["sistema"]

        db.collection(
            "dispositivos"
        ).add({

            "nombre": nombre,
            "correo": correo,
            "dispositivo": dispositivo,
            "sistema": sistema,
            "acceso": "28/05/2026 12:00",
            "estado": "Activo"

        })

    except Exception as e:

        print(e)

    return redirect("/gestiondisp")

# =========================================
# BLOQUEAR DISPOSITIVO
# =========================================

@gestiondisp_bp.route("/bloquear_dispositivo/<id>")
def bloquear_dispositivo(id):

    try:

        dispositivo_ref = db.collection(
            "dispositivos"
        ).document(id)

        dispositivo_ref.update({

            "estado": "Bloqueado"

        })

    except Exception as e:

        print(e)

    return redirect("/gestiondisp")