from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from pymongo import MongoClient
import pandas as pd
from openpyxl import Workbook
from werkzeug.utils import secure_filename
from io import BytesIO
import io
import os
from bson import ObjectId

app = Flask(__name__)
CORS(app, origins=["http://localhost:5501", "http://127.0.0.1:5500", "http://10.40.24.125:5500"])   # Esto habilita CORS para permitir peticiones desde otros orígenes

# Configuración de la carga de archivos
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
# Conexión a MongoDB
mongo_uri = "mongodb+srv://anacato:nacato1@cluster0.sdefz.mongodb.net/?retryWrites=true&w=majority"
try:
    client = MongoClient(mongo_uri)
    db = client['cliente']  # Nombre de la base de datos
    clientes_collection = db['clientes']  # Nombre de la colección
    productos_collection = db['productos']  
    ventas_collection = db['ventas']
    categorias_collection = db['categorias']
    print("Conexión exitosa a MongoDB!")
except Exception as e:
    print(f"Error al conectar a MongoDB: {e}")
    exit()  # Salimos si no podemos conectar a la base de datos


@app.route('/agregar-cliente', methods=['POST'])
def agregar_cliente():
    data = request.get_json()
    if not data.get('nombre') or not data.get('telefono') or not data.get('email'):
        return jsonify({'message': 'Faltan datos necesarios'}), 400

    cliente = {
        "nombre": data.get('nombre'),
        "telefono": data.get('telefono'),
        "email": data.get('email')
    }

    try:
        clientes_collection.insert_one(cliente)
        return jsonify({'message': 'Cliente agregado exitosamente'}), 201
    except Exception as e:
        return jsonify({'message': f'Error al agregar cliente: {str(e)}'}), 500


@app.route('/modificar-cliente', methods=['PUT'])
def modificar_cliente():
    data = request.get_json()

    if not data.get('id') or not data.get('nombre') or not data.get('telefono') or not data.get('email'):
        return jsonify({'message': 'Faltan datos necesarios'}), 400

    try:
        # Convertir el ID a ObjectId
        cliente_id = ObjectId(data['id'])

        result = clientes_collection.update_one(
            {'_id': cliente_id},  # Usar ObjectId aquí
            {'$set': {'nombre': data['nombre'], 'telefono': data['telefono'], 'email': data['email']}}
        )
        
        if result.matched_count > 0:
            return jsonify({'message': 'Cliente modificado exitosamente'}), 200
        else:
            return jsonify({'message': 'Cliente no encontrado'}), 404
    except Exception as e:
        return jsonify({'message': f'Error al modificar cliente: {str(e)}'}), 500


@app.route('/eliminar-cliente', methods=['DELETE'])
def eliminar_cliente():
    data = request.get_json()

    if not data.get('id'):
        return jsonify({'message': 'Falta el ID del cliente'}), 400

    try:
        # Convertir el ID a ObjectId
        cliente_id = ObjectId(data['id'])

        result = clientes_collection.delete_one({'_id': cliente_id})  # Usar ObjectId aquí

        if result.deleted_count > 0:
            return jsonify({'message': 'Cliente eliminado exitosamente'}), 200
        else:
            return jsonify({'message': 'Cliente no encontrado'}), 404
    except Exception as e:
        return jsonify({'message': f'Error al eliminar cliente: {str(e)}'}), 500
    


@app.route('/agregar-producto', methods=['POST'])
def agregar_producto():
    try:
        data = request.get_json()

        # Verificar que los datos necesarios estén presentes
        if 'proveedor' not in data or 'producto' not in data or 'precio' not in data or 'cantidad' not in data:
            return jsonify({"error": "Faltan datos requeridos"}), 400

        # Crear el producto en la base de datos
        producto = {
            "proveedor": data["proveedor"],
            "producto": data["producto"],
            "precio": data["precio"],
            "cantidad": data["cantidad"]
        }

        # Insertar el producto en la base de datos
        result = productos_collection.insert_one(producto)

        return jsonify({"message": "Producto agregado exitosamente", "id": str(result.inserted_id)}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para modificar un producto
@app.route('/modificar-producto', methods=['PUT'])
def modificar_producto():
    try:
        data = request.get_json()

        # Verificar que se haya proporcionado el ID y los datos requeridos
        if 'id' not in data or 'proveedor' not in data or 'producto' not in data or 'precio' not in data or 'cantidad' not in data:
            return jsonify({"error": "Faltan datos requeridos"}), 400

        # Buscar el producto por ID
        producto_id = ObjectId(data['id'])
        producto = productos_collection.find_one({"_id": producto_id})

        if not producto:
            return jsonify({"error": "Producto no encontrado"}), 404

        # Actualizar el producto en la base de datos
        updated_data = {
            "proveedor": data["proveedor"],
            "producto": data["producto"],
            "precio": data["precio"],
            "cantidad": data["cantidad"]
        }

        productos_collection.update_one({"_id": producto_id}, {"$set": updated_data})

        return jsonify({"message": "Producto modificado exitosamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para eliminar un producto
@app.route('/eliminar-producto', methods=['DELETE'])
def eliminar_producto():
    try:
        data = request.get_json()

        # Verificar que se haya proporcionado el ID
        if 'id' not in data:
            return jsonify({"error": "ID del producto es requerido"}), 400

        # Buscar el producto por ID
        producto_id = ObjectId(data['id'])
        producto = productos_collection.find_one({"_id": producto_id})

        if not producto:
            return jsonify({"error": "Producto no encontrado"}), 404

        # Eliminar el producto de la base de datos
        productos_collection.delete_one({"_id": producto_id})

        return jsonify({"message": "Producto eliminado exitosamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

    # Obtener lista de clientes
@app.route('/get-clientes', methods=['GET'])
def get_clientes():
    clientes = list(clientes_collection.find())
    for cliente in clientes:
        cliente['_id'] = str(cliente['_id'])
    return jsonify(clientes)

# Obtener lista de productos
@app.route('/get-productos', methods=['GET'])
def get_productos():
    productos = list(productos_collection.find())
    for producto in productos:
        producto['_id'] = str(producto['_id'])
    return jsonify(productos)

# Registrar venta
@app.route('/registrar-venta', methods=['POST'])
def registrar_venta():
    try:
        data = request.get_json()
        cliente_id = ObjectId(data['clienteId'])
        producto_id = ObjectId(data['productoId'])
        cantidad = int(data['cantidad'])
        
        cliente = clientes_collection.find_one({"_id": cliente_id})
        producto = productos_collection.find_one({"_id": producto_id})

        if not cliente or not producto:
            return jsonify({"error": "Cliente o producto no encontrado"}), 404

        # Registrar la venta
        venta = {
            "cliente_id": cliente_id,
            "producto_id": producto_id,
            "cantidad": cantidad,
            "fecha": pd.to_datetime('today').strftime('%Y-%m-%d')  # Fecha actual
        }
        
        ventas_collection.insert_one(venta)
        
        # Reducir la cantidad del producto
        productos_collection.update_one({"_id": producto_id}, {"$inc": {"cantidad": -cantidad}})
        
        return jsonify({"message": "Venta registrada exitosamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Generar reporte de ventas
@app.route('/generar-reporte-ventas', methods=['GET'])
def generar_reporte_ventas():
    try:
        ventas = list(ventas_collection.find())
        wb = Workbook()
        ws = wb.active
        ws.title = "Reporte de Ventas"
        ws.append(["Fecha", "Cliente", "Producto", "Cantidad"])

        for venta in ventas:
            cliente = clientes_collection.find_one({"_id": venta["cliente_id"]})
            producto = productos_collection.find_one({"_id": venta["producto_id"]})
            ws.append([venta["fecha"], cliente["nombre"], producto["producto"], venta["cantidad"]])

        archivo = BytesIO()
        wb.save(archivo)
        archivo.seek(0)

        return send_file(archivo, as_attachment=True, download_name="reporte_ventas.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/reporte-clientes', methods=['GET'])
def generar_reporte():
    try:
        # Obtener todos los clientes de la colección
        clientes = clientes_collection.find()

        # Crear un libro de Excel
        wb = Workbook()
        ws = wb.active
        ws.title = "Reporte de Clientes"

        # Encabezados para el reporte
        ws.append(["Nombre", "Edad", "Correo", "Teléfono", "Carrito", "Pago"])

        # Agregar los datos de los clientes
        for cliente in clientes:
            ws.append([cliente['Nombre'], cliente['Edad'], cliente['Correo'], cliente['Telefono'], len(cliente['Carrito']), len(cliente['Pago'])])

        # Crear un objeto en memoria para guardar el archivo
        archivo = BytesIO()
        wb.save(archivo)
        archivo.seek(0)

        # Enviar el archivo Excel al frontend
        return send_file(archivo, as_attachment=True, download_name="reporte_clientes.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    except Exception as e:
        print(f"Error generando el reporte: {str(e)}")
        return jsonify({"error": "No se pudo generar el reporte"}), 500

if __name__ == '__main__':
    app.run(debug=True)

