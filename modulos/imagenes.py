# =====================================================
# MODULO IMAGENES
# SISTEMA REPORTES CIUDADANOS
# =====================================================
from modulos.imagenes import imagenes_bp
from flask import Blueprint, render_template, request, redirect, url_for, flash
from firebase_admin import storage, firestore
import os

# =====================================================
# BLUEPRINT
# =====================================================

imagenes_bp = Blueprint(
    'imagenes',
    __name__
)

# =====================================================
# FIREBASE
# =====================================================

db = firestore.client()
bucket = storage.bucket()

# =====================================================
# CARPETA LOCAL
# =====================================================

CARPETA = "static/img"

if not os.path.exists(CARPETA):
    os.makedirs(CARPETA)

# =====================================================
# MOSTRAR PAGINA
# =====================================================

@imagenes_bp.route('/imagenes')
def imagenes():

    lista_evidencias = []

    try:

        evidencias = db.collection("evidencias").stream()

        for evidencia in evidencias:

            datos = evidencia.to_dict()

            lista_evidencias.append(datos)

    except Exception as e:

        print("Error:", e)

    return render_template(
        'imagenes.html',
        evidencias=lista_evidencias
    )

# =====================================================
# SUBIR IMAGENES
# =====================================================

@imagenes_bp.route('/subir_imagenes', methods=['POST'])
def subir_imagenes():

    try:

        archivos = request.files.getlist('imagenes')

        if len(archivos) == 0:

            flash(
                "Selecciona al menos una imagen",
                "warning"
            )

            return redirect(url_for('imagenes.imagenes'))

        cantidad = 0

        for archivo in archivos:

            if archivo.filename == '':
                continue

            nombre = archivo.filename

            ruta_local = os.path.join(
                CARPETA,
                nombre
            )

            # =========================================
            # GUARDAR LOCAL
            # =========================================

            archivo.save(ruta_local)

            # =========================================
            # FIREBASE STORAGE
            # =========================================

            blob = bucket.blob(
                f"evidencias/{nombre}"
            )

            blob.upload_from_filename(
                ruta_local
            )

            blob.make_public()

            url = blob.public_url

            # =========================================
            # FIRESTORE
            # =========================================

            datos = {
                "nombre": nombre,
                "url": url
            }

            db.collection(
                "evidencias"
            ).add(datos)

            cantidad += 1

        flash(
            f"{cantidad} imagen(es) subida(s) correctamente",
            "success"
        )

    except Exception as e:

        flash(str(e), "danger")

    return redirect(
        url_for('imagenes.imagenes')
    )