from flask import (
    Blueprint,
    request,
    redirect,
    flash,
    render_template
)

# Importa Firestore de Firebase
from firebase_admin import firestore

# Importa manejo de fechas
from datetime import datetime

# Importa función para registrar auditoría
from modulos.auditoria import registrar_evento

# Importa librería para manejo de carpetas/rutas
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
# MOSTRAR PAGINA
# =====================================

@imagenes_bp.route(
    "/imagenes",
    methods=["GET", "POST"]
)

def imagenes():

    # =====================================
    # SI ES POST SUBE IMAGENES
    # =====================================

    if request.method == "POST":

        return procesar_imagenes()

    # =====================================
    # LISTA EVIDENCIAS
    # =====================================

    lista_evidencias = []

    try:

        evidencias = db.collection(
            "evidencias"
        ).stream()

        for evidencia in evidencias:

            datos = evidencia.to_dict()

            lista_evidencias.append(
                datos
            )

    except Exception as e:

        print(
            "Error:",
            e
        )

    return render_template(

        "imagenes.html",

        evidencias=lista_evidencias

    )

# =====================================
# SUBIR IMAGENES
# =====================================

def procesar_imagenes():

    try:

        archivos = request.files.getlist(
            "imagenes"
        )

        # =====================================
        # VALIDAR
        # =====================================

        if len(archivos) == 0:

            flash(
                "Selecciona al menos una imagen",
                "warning"
            )

            return redirect("/imagenes")

        cantidad = 0

        # =====================================
        # RECORRER ARCHIVOS
        # =====================================

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

            archivo.save(
                ruta_local
            )

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

                "reporte_id":
                reporte_id,

                "nombre":
                nombre,

                "url":
                url,

                "fecha":
                fecha_actual

            }

            referencia.set(
                datos
            )

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

        # =====================================
        # MENSAJE
        # =====================================

        flash(

            f"{cantidad} imagen(es) subida(s) correctamente",

            "success"

        )

    except Exception as e:

        flash(

            f"Error: {str(e)}",

            "danger"

        )

    return redirect(
        "/imagenes"
    )