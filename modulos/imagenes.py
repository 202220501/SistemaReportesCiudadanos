from flask import (
    Blueprint,
    request,
    redirect,
    flash
)

from firebase_admin import firestore

from datetime import datetime

from modulos.auditoria import registrar_evento

import os

# =====================================
# BLUEPRINT
# =====================================

imagenes_bp = Blueprint(
    "imagenes",
    __name__
)

# =====================================
# FIREBASE
# =====================================

db = firestore.client()

# =====================================
# CARPETA LOCAL
# =====================================

CARPETA = "static/img"

if not os.path.exists(CARPETA):

    os.makedirs(CARPETA)

# =====================================
# SUBIR IMAGENES
# =====================================

def procesar_imagenes():

    try:

        archivos = request.files.getlist(
            "imagenes"
        )

        if len(archivos) == 0:

            flash(
                "Selecciona al menos una imagen",
                "warning"
            )

            return redirect("/imagenes")

        cantidad = 0

        for archivo in archivos:

            if archivo.filename == "":

                continue

            # =====================================
            # NOMBRE
            # =====================================

            nombre = archivo.filename

            ruta_local = os.path.join(
                CARPETA,
                nombre
            )

            # =====================================
            # GUARDAR LOCAL
            # =====================================

            archivo.save(ruta_local)

            # =====================================
            # URL LOCAL
            # =====================================

            url = f"/static/img/{nombre}"

            # =====================================
            # FECHA
            # =====================================

            fecha_actual = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            # =====================================
            # FIRESTORE
            # =====================================

            referencia = db.collection(
                "evidencias"
            ).document()

            reporte_id = referencia.id

            datos = {

                "reporte_id": reporte_id,

                "url": url,

                "fecha": fecha_actual

            }

            referencia.set(datos)
            # =====================================
            # AUDITORIA
            # =====================================

            registrar_evento(

            nombre,

            "SUBIR_IMAGEN",

            "imagenes",

            "Se subió la imagen"
            )
            
            cantidad += 1

        flash(
            f"{cantidad} imagen(es) subida(s) correctamente",
            "success"
        )

    except Exception as e:

        flash(
            f"Error: {str(e)}",
            "danger"
        )

    return redirect("/imagenes")