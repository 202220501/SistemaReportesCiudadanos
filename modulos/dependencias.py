from firebase_config import db
from flask import Blueprint, render_template, request, redirect, flash

dependencias_bp = Blueprint('dependencias', __name__)

# ✅ MOSTRAR Y AGREGAR
@dependencias_bp.route('/dependencias', methods=['GET', 'POST'])
def dependencias():

    if request.method == 'POST':
        nombre = request.form['nombre']
        zona = request.form['zona']
        tipo_servicio = request.form['tipo_servicio']

        # ✅ VALIDACIONES BACKEND
        if not nombre or not zona or not tipo_servicio:
            flash("Todos los campos son obligatorios", "danger")
            return redirect('/dependencias')

        if len(nombre) < 3:
            flash("El nombre debe tener mínimo 3 caracteres", "warning")
            return redirect('/dependencias')

        # ✅ GUARDAR EN FIREBASE
        db.collection('dependencias').add({
            'nombre': nombre,
            'zona': zona,
            'tipo_servicio': tipo_servicio
        })

        # ✅ MENSAJE
        flash("Dependencia guardada correctamente ✅", "success")

        return redirect('/dependencias')

    # ✅ OBTENER DATOS
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

    # ✅ MENSAJE
    flash("Dependencia eliminada correctamente 🗑️", "danger")

    return redirect('/dependencias')


# ✅ EDITAR
@dependencias_bp.route('/editar_dependencia/<id>', methods=['POST'])
def editar_dependencia(id):

    nombre = request.form['nombre']
    zona = request.form['zona']
    tipo_servicio = request.form['tipo_servicio']

    # ✅ VALIDACIONES
    if not nombre or not zona or not tipo_servicio:
        flash("Todos los campos son obligatorios", "danger")
        return redirect('/dependencias')

    if len(nombre) < 3:
        flash("El nombre debe tener mínimo 3 caracteres", "warning")
        return redirect('/dependencias')

    # ✅ ACTUALIZAR FIREBASE
    db.collection('dependencias').document(id).update({
        'nombre': nombre,
        'zona': zona,
        'tipo_servicio': tipo_servicio
    })

    # ✅ MENSAJE
    flash("Dependencia actualizada correctamente ✏️", "warning")

    return redirect('/dependencias')