# =====================================================
# PANEL ADMINISTRATIVO
# FLASK + FIREBASE
# =====================================================
from modulos.admin import admin_bp
from flask import Blueprint, render_template, request
from firebase_admin import firestore

# =====================================================
# BLUEPRINT
# =====================================================

admin_bp = Blueprint(
    'admin',
    __name__
)

# =====================================================
# FIREBASE
# =====================================================

db = firestore.client()

coleccion_reportes = db.collection(
    'reportes'
)

# =====================================================
# PANEL ADMIN
# =====================================================

@admin_bp.route('/admin')
def panel_admin():

    filtro = request.args.get(
        'filtro',
        'Todos'
    )

    lista_reportes = []

    try:

        # =========================================
        # FILTRO
        # =========================================

        if filtro == "Todos":

            docs = coleccion_reportes.stream()

        else:

            docs = coleccion_reportes.where(
                'estado',
                '==',
                filtro
            ).stream()

        # =========================================
        # RECORRER REPORTES
        # =========================================

        for doc in docs:

            datos = doc.to_dict()

            datos['id'] = doc.id

            lista_reportes.append(datos)

    except Exception as e:

        print("MIS REPORTES DE FIREBASE:", lista_reportes)

    return render_template(

        'admin.html',

        reportes=lista_reportes,
        filtro=filtro

    )