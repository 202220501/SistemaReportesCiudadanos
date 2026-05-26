import firebase_admin
from firebase_admin import credentials, firestore

# Evita inicializar Firebase más de una vez
if not firebase_admin._apps:

    cred = credentials.Certificate("clave.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()