from flask import Flask, request, jsonify, send_file
import csv
import io
import os
import uuid
from werkzeug.wsgi import FileWrapper

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def json_to_csv():
    try:
        # Obtener los datos JSON del cuerpo de la solicitud
        json_data = request.get_json()

        # Verificar si se recibieron datos
        if not json_data:
            return jsonify({'error': 'No se recibieron datos JSON'}), 400

        # Supongamos que el JSON es una lista de diccionarios con las mismas claves
        # y queremos convertirlo a CSV
        keys = json_data[0].keys() if json_data else []
        
        # Generar un nombre único para el archivo CSV
        unique_filename = f"datos_{str(uuid.uuid4())[:8]}.csv"

        # Ruta para guardar el archivo CSV temporalmente
        csv_file_path = unique_filename

        # Generar el archivo CSV en disco
        with open(csv_file_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=keys)

            # Escribir encabezados
            writer.writeheader()

            # Escribir filas de datos
            writer.writerows(json_data)

        # Devolver el enlace para descargar el archivo CSV
        return jsonify({'success': True, 'csv_link': f"/download/{csv_file_path}"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<path:file_path>', methods=['GET'])
def download(file_path):
    try:
        # Verificar si el archivo existe
        if os.path.exists(file_path):
            # Enviar el archivo para su descarga
            with open(file_path, 'rb') as f:
                wrapper = FileWrapper(f)
                response = app.response_class(wrapper, mimetype='text/csv', direct_passthrough=True)
                response.headers['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'

            # Eliminar el archivo después de la descarga
            os.remove(file_path)

            return response
        else:
            return jsonify({'error': 'El archivo no existe'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
