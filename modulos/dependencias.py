from firebase_config import db
from flask import Blueprint, render_template, request, redirect

dependencias_bp = Blueprint('dependencias', _name_)

# ✅ MOSTRAR Y AGREGAR
@dependencias_bp.route('/dependencias', methods=['GET', 'POST'])
def dependencias():

    if request.method == 'POST':
        nombre = request.form['nombre']
        zona = request.form['zona']
        tipo_servicio = request.form['tipo_servicio']

        db.collection('dependencias').add({
            'nombre': nombre,
            'zona': zona,
            'tipo_servicio': tipo_servicio
        })

        return redirect('/dependencias')

    deps = []
    docs = db.collection('dependencias').stream()

    for doc in docs:
        d = doc.to_dict()
        d['id_dependencia'] = doc.id
        deps.append(d)

    return render_template('dependencias.html', dependencias=deps)


# ✅ ELIMINAR
@dependencias_bp.route('/eliminar_dependencia/<id>')
def eliminar_dependencia(id):
    db.collection('dependencias').document(id).delete()
    return redirect('/dependencias')