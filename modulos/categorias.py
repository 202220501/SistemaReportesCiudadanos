# =====================================================
# MODULO CATEGORIAS
# FLASK + FIREBASE CRUD
# =====================================================

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from firebase_admin import firestore

# =====================================================
# BLUEPRINT
# =====================================================

categorias_bp = Blueprint(
    'categorias',
    __name__
)

# =====================================================
# FIREBASE
# =====================================================

db = firestore.client()

# =====================================================
# MOSTRAR PAGINA
# =====================================================

@categorias_bp.route('/categorias')
def categorias():

    lista_categorias = []

    try:

        categorias_db = db.collection(
            "categorias"
        ).stream()

        for categoria in categorias_db:

            datos = categoria.to_dict()

            datos["id"] = categoria.id

            lista_categorias.append(datos)

    except Exception as e:

        print(e)

    return render_template(
        'categorias.html',
        categorias=lista_categorias
    )

# =====================================================
# AGREGAR CATEGORIA
# =====================================================

@categorias_bp.route(
    '/agregar_categoria',
    methods=['POST']
)
def agregar_categoria():

    try:

        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        icono = request.form.get('icono')

        if not nombre or not descripcion:

            flash(
                "Completa todos los campos",
                "warning"
            )

            return redirect(
                url_for('categorias.categorias')
            )

        categoria = {

            "nombre": nombre,
            "descripcion": descripcion,
            "icono": icono

        }

        db.collection(
            "categorias"
        ).add(categoria)

        flash(
            "Categoría agregada correctamente",
            "success"
        )

    except Exception as e:

        flash(str(e), "danger")

    return redirect(
        url_for('categorias.categorias')
    )

# =====================================================
# ACTUALIZAR CATEGORIA
# =====================================================

@categorias_bp.route(
    '/actualizar_categoria/<id_categoria>',
    methods=['POST']
)
def actualizar_categoria(id_categoria):

    try:

        nuevo_nombre = request.form.get('nombre')
        nueva_descripcion = request.form.get('descripcion')
        nuevo_icono = request.form.get('icono')

        if not nuevo_nombre or not nueva_descripcion:

            flash(
                "Completa todos los campos",
                "warning"
            )

            return redirect(
                url_for('categorias.categorias')
            )

        db.collection(
            "categorias"
        ).document(id_categoria).update({

            "nombre": nuevo_nombre,
            "descripcion": nueva_descripcion,
            "icono": nuevo_icono

        })

        flash(
            "Categoría actualizada correctamente",
            "success"
        )

    except Exception as e:

        flash(str(e), "danger")

    return redirect(
        url_for('categorias.categorias')
    )

# =====================================================
# ELIMINAR CATEGORIA
# =====================================================

@categorias_bp.route(
    '/eliminar_categoria/<id_categoria>'
)
def eliminar_categoria(id_categoria):

    try:

        db.collection(
            "categorias"
        ).document(id_categoria).delete()

        flash(
            "Categoría eliminada correctamente",
            "success"
        )

    except Exception as e:

        flash(str(e), "danger")

    return redirect(
        url_for('categorias.categorias')
    )