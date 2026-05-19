from flask import Blueprint, render_template, request, redirect, url_for, flash
from firebase_config import db

# Definir el blueprint para el modulo de votos
votos_bp = Blueprint('votos', __name__)

@votos_bp.route('/votos')
def listar_votos():
    try:
        # Obtenemos todos los reportes de la coleccion de Firebase
        # [cite: 406]
        reportes_ref = db.collection('reportes')
        docs = reportes_ref.stream()
        
        lista_reportes = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            # Si el reporte no tiene campo de votos, lo inicializamos en 0
            if 'votos' not in data:
                data['votos'] = 0
            lista_reportes.append(data)
            
        return render_template('votos.html', reportes=lista_reportes)
    except Exception as e:
        flash(f"Error al cargar reportes: {str(e)}", "danger")
        return redirect(url_for('index'))

@votos_bp.route('/votar/<reporte_id>', methods=['POST'])
def votar_reporte(reporte_id):
    try:
        # Referencia al documento especifico en Firestore [cite: 404]
        reporte_ref = db.collection('reportes').document(reporte_id)
        reporte = reporte_ref.get()

        if reporte.exists:
            votos_actuales = reporte.to_dict().get('votos', 0)
            # Incrementamos el voto
            reporte_ref.update({'votos': votos_actuales + 1})
            flash("Voto registrado correctamente", "success") # [cite: 401]
        else:
            flash("El reporte no existe", "danger") # [cite: 400]
            
    except Exception as e:
        flash(f"Error al votar: {str(e)}", "danger") # [cite: 398]
        
    return redirect(url_for('votos.listar_votos'))