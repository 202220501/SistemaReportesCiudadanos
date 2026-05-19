from flask import Flask, render_template, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore

# MODIFICACIÓN 1: Le decimos a Flask que la carpeta templates está afuera (..)
app = Flask(__name__, template_folder='../templates')

# =====================================================
# CONFIGURACIÓN DE FIREBASE DIRECTA
# =====================================================
try:
    # MODIFICACIÓN 2: La llave key.json también está afuera de la carpeta modulos
    cred = credentials.Certificate("../key.json") 
    
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("✅ Conexión exitosa a la base de datos Firestore")
except Exception as e:
    print(f"❌ Error de conexión: {e}")

# =====================================================
# RUTAS WEB
# =====================================================
@app.route('/gps')
def mostrar_mapa():
    # Ahora sí encontrará el archivo en /templates/Ubicacion.html
    return render_template('Ubicacion.html')

@app.route('/guardar_gps', methods=['POST'])
def guardar_gps():
    datos = request.json
    try:
        reporte_ref = db.collection('reportes_ubicacion').document()
        reporte_ref.set({
            'titulo': datos['titulo'],
            'ubicacion': firestore.GeoPoint(float(datos['lat']), float(datos['lng'])),
            'timestamp': firestore.SERVER_TIMESTAMP
        })
        return jsonify({"mensaje": "✅ Ubicación guardada en Firebase"}), 200
    except Exception as e:
        return jsonify({"mensaje": f"❌ Error al guardar: {str(e)}"}), 400

# =====================================================
# ARRANQUE DEL SERVIDOR
# =====================================================
if __name__ == '__main__':
    app.run(debug=True)