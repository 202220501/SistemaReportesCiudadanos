from flask import Flask, render_template, request, jsonify, redirect
import firebase_admin
from firebase_admin import credentials, firestore

# Configuración para buscar la carpeta templates afuera
app = Flask(__name__, template_folder='../templates')

# =====================================================
# CONFIGURACIÓN DE FIREBASE DIRECTA
# =====================================================
try:
    cred = credentials.Certificate("clave.json") 
    
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("✅ Conexión exitosa a la base de datos Firestore")
except Exception as e:
    print(f"❌ Error de conexión: {e}")

# =====================================================
# RUTAS WEB
# =====================================================

# Si entras a la raíz (http://127.0.0.1:5001/), te redirige al mapa automáticamente
@app.route('/')
def inicio():
    return redirect('/gps')

@app.route('/gps')
def mostrar_mapa():
    return render_template('gps.html')

@app.route('/guardar_gps', methods=['POST'])
def guardar_gps():
    datos = request.json
    try:
        reporte_ref = db.collection('reportes').document()
        
        reporte_ref.set({
            'id_usuario': 1,                            
            'id_categoria': datos.get('id_categoria', 1), 
            'id_estado_actual': 1,                      
            'descripcion': datos.get('titulo', 'Sin descripción'), 
            'direccion': datos.get('direccion', 'Sin dirección'),
            'latitud': float(datos['lat']),
            'longitud': float(datos['lng']),
            'prioridad': datos.get('prioridad', 'Normal'),
            'votos_totales': 0,                         
            'fecha_creacion': firestore.SERVER_TIMESTAMP,
            'fecha_actualizacion': firestore.SERVER_TIMESTAMP
        })
        
        return jsonify({"mensaje": "✅ Ubicación guardada con la estructura oficial del diagrama"}), 200
    except Exception as e:
        return jsonify({"mensaje": f"❌ Error al guardar en la base de datos: {str(e)}"}), 400

# =====================================================
# RUTA PARA LEER LA BASE DE DATOS
# =====================================================
@app.route('/ver_reportes', methods=['GET'])
def ver_reportes():
    try:
        # Obtenemos en tiempo real los documentos almacenados con la clave.json
        reportes_ref = db.collection('reportes').stream()
        lista_reportes = []
        
        for doc in reportes_ref:
            data = doc.to_dict()
            data['id_documento'] = doc.id
            lista_reportes.append(data)
            
        return jsonify(lista_reportes), 200
    except Exception as e:
        return jsonify({"error": f"No se pudo leer la base de datos: {str(e)}"}), 400

# =====================================================
# ARRANQUE DEL SERVIDOR
# =====================================================
if __name__ == '__main__':
    # Arranca en el puerto 5001 para ser independiente del equipo
    app.run(debug=True, port=5001)