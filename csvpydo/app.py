from flask import Flask, request, jsonify, send_file
import pandas as pd
import os
import uuid

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def json_to_csv():
    try:
        # Obtener los datos JSON del cuerpo de la solicitud
        json_data = request.get_json()

        # Verificar si se recibieron datos
        if not json_data:
            return jsonify({'error': 'No se recibieron datos JSON'}), 400

        # Verificar si el JSON es una lista de diccionarios no vacía
        if not isinstance(json_data, list) or not json_data:
            return jsonify({'error': 'Se esperaba una lista no vacía de diccionarios'}), 400

        # Crear un DataFrame de Pandas a partir de los datos JSON
        df = pd.DataFrame(json_data)

        # Generar un nombre único para el archivo CSV
        unique_filename = f"datos_{str(uuid.uuid4())[:8]}.csv"

        # Ruta para guardar el archivo CSV temporalmente
        csv_file_path = unique_filename

        # Guardar el DataFrame como archivo CSV
        df.to_csv(csv_file_path, index=False)

        # Devolver el enlace para descargar el archivo CSV
        return jsonify({'success': True, 'csv_link': f"/download/{csv_file_path}", 'delete_link': f"/delete/{csv_file_path}"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<path:file_path>', methods=['GET'])
def download(file_path):
    try:
        # Verificar si el archivo existe
        if os.path.exists(file_path):
            # Enviar el archivo para su descarga
            response = send_file(file_path, as_attachment=True)
            
            return response
        else:
            return jsonify({'error': 'El archivo no existe'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete/<path:file_path>', methods=['GET'])
def delete_file(file_path):
    try:
        # Verificar si el archivo existe
        if os.path.exists(file_path):
            # Eliminar el archivo
            os.remove(file_path)
            
            return jsonify({'success': True, 'message': 'Archivo eliminado correctamente'})
        else:
            return jsonify({'error': 'El archivo no existe'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
