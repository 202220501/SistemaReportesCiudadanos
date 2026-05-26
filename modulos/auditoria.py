from flask import Blueprint, render_template
from firebase_admin import firestore
from datetime import datetime

# ==========================================
# BLUEPRINT
# ==========================================

auditoria_bp = Blueprint(
    'auditoria',
    __name__
)

# ==========================================
# FIRESTORE
# ==========================================

db = firestore.client()

# ==========================================
# REGISTRAR EVENTO
# ==========================================

def registrar_evento(
    usuario,
    accion,
    modulo,
    descripcion
):

    datos = {

        "usuario": usuario,

        "accion": accion,

        "modulo": modulo,

        "descripcion": descripcion,

        "fecha": datetime.now().strftime(
            "%d/%m/%Y %H:%M:%S"
        )

    }

    db.collection(
        "auditoria"
    ).add(datos)

# ==========================================
# MOSTRAR AUDITORIA
# ==========================================

@auditoria_bp.route('/auditoria')
def auditoria():

    lista_eventos = []

    eventos = db.collection(
        "auditoria"
    ).stream()

    for evento in eventos:

        lista_eventos.append(
            evento.to_dict()
        )

    return render_template(
        'auditoria.html',
        eventos=lista_eventos
    )