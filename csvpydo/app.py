from flask import Flask, request, jsonify, send_file
import pandas as pd
import os
import uuid
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/convert', methods=['POST'])
def json_to_csv():
    try:
        json_data = request.get_json()

        if not json_data:
            return jsonify({'error': 'No se recibieron datos JSON'}), 400

        if not isinstance(json_data, dict):
            return jsonify({'error': 'Se esperaba un JSON con claves de listas de productos'}), 400

        success_links = {}
        for key, value in json_data.items():
            if isinstance(value, list):
                df = pd.DataFrame(value)
                unique_filename = f"{key}_{str(uuid.uuid4())[:8]}.csv"
                csv_file_path = os.path.join(os.getcwd(), unique_filename)
                df.to_csv(csv_file_path, index=False)

                generate_link = f"/generate/{unique_filename}"
                delete_link = f"/delete/{unique_filename}"

                # Agregar los enlaces al diccionario success_links
                success_links = {
                    'generate_link': generate_link,
                    'delete_link': delete_link
                }

        return jsonify({
            'success': True,
            'download_links': success_links
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate/<path:file_path>', methods=['GET'])
def generate(file_path):
    try:
        csv_file_path = os.path.join(os.getcwd(), file_path)

        if os.path.exists(csv_file_path):
            return send_file(csv_file_path, as_attachment=True)
        else:
            return jsonify({'error': 'El archivo no existe'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete/<path:file_path>', methods=['GET'])
def delete(file_path):
    try:
        csv_file_path = os.path.join(os.getcwd(), file_path)

        if os.path.exists(csv_file_path):
            os.remove(csv_file_path)
            return jsonify({'success': True, 'message': 'Archivo eliminado correctamente'})
        else:
            return jsonify({'error': 'El archivo no existe'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
