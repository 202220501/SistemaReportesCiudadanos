# =====================================================
# PANEL ADMINISTRATIVO
# FLASK + FIREBASE
# =====================================================
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
        elif filtro == "Pendiente":
            # Buscamos estado_id "1" en lugar de la palabra "Pendiente"
            docs = coleccion_reportes.where('estado_id', '==', '1').stream()
        elif filtro == "Atendido":
            # Asumiendo que el "2" es para los Atendidos
            docs = coleccion_reportes.where('estado_id', '==', '2').stream()

        # =========================================
        # RECORRER REPORTES
        # =========================================
        for doc in docs:

            datos = doc.to_dict()
            
            # Guardamos el ID único del documento de Firebase por si lo necesitas después
            datos['id'] = doc.id

            lista_reportes.append(datos)
            
        # Print de depuración para que veas en tu terminal negra qué está llegando
        print("MIS REPORTES DE FIREBASE:", lista_reportes)

    except Exception as e:
        
        # Si algo falla con la base de datos, te avisará aquí
        print("ERROR CON FIREBASE:", e)

    return render_template(
        'admin.html',
        reportes=lista_reportes,
        filtro=filtro
    )