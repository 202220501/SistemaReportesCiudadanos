from firebase_config import db

def guardar_usuario(nombre, correo):

    db.collection("usuarios").add({
        "nombre": nombre,
        "correo": correo
    })

    print("Usuario guardado")