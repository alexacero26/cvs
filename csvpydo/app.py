from flask import Flask, request, jsonify, send_file
import pandas as pd
import os
import uuid
import json

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def json_to_csv():
    try:
        # Obtener los datos JSON del cuerpo de la solicitud o del parámetro json_data si está presente
        json_data = request.get_json()
        if not json_data:
            json_data = request.form.get('json_data')

        # Verificar si se recibieron datos
        if not json_data:
            return jsonify({'error': 'No se recibieron datos JSON'}), 400

        # Convertir el parámetro JSON a un diccionario si es una cadena
        if isinstance(json_data, str):
            json_data = json.loads(json_data)

        # Verificar si el JSON es una lista de diccionarios no vacía
        if not isinstance(json_data, list) or not json_data:
            return jsonify({'error': 'Se esperaba una lista no vacía de diccionarios'}), 400

        # Crear un DataFrame de Pandas a partir de los datos JSON
        df = pd.DataFrame(json_data)

        # Generar un nombre único para el archivo CSV
        unique_filename = f"datos_{str(uuid.uuid4())[:8]}.csv"

        # Ruta para guardar el archivo CSV en el directorio actual
        csv_file_path = os.path.join(os.getcwd(), unique_filename)

        # Guardar el DataFrame como archivo CSV
        df.to_csv(csv_file_path, index=False)

        # Devolver los enlaces para generar, descargar y eliminar el archivo CSV
        generate_link = f"/generate/{unique_filename}"
        delete_link = f"/delete/{unique_filename}"

        return jsonify({
            'success': True,
            'generate_link': generate_link,
            'delete_link': delete_link
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Las rutas '/generate' y '/delete' se mantienen iguales...

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



