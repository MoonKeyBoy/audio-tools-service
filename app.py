from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

# On définit le dossier de base où se trouvent nos fichiers
# Ce sera le point de montage de notre volume partagé
BASE_DIR = "/media"

@app.route('/split', methods=['POST'])
def split_audio():
    data = request.get_json()
    if not data or 'file_path' not in data:
        return jsonify({"error": "Missing file_path"}), 400

    # On construit le chemin complet et sécurisé du fichier
    relative_path = data['file_path']
    input_file = os.path.join(BASE_DIR, relative_path)
    
    if not os.path.exists(input_file):
        return jsonify({"error": f"File not found: {input_file}"}), 404

    output_dir = os.path.dirname(input_file)
    output_pattern = os.path.join(output_dir, "chunk_%03d.mp3")

    command = [
        'ffmpeg',
        '-i', input_file,
        '-f', 'segment',
        '-segment_time', '870',
        '-c', 'copy',
        output_pattern
    ]

    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        return jsonify({"status": "success", "message": f"File split into chunks in {output_dir}"}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "FFmpeg command failed", "details": e.stderr}), 500

@app.route('/duration', methods=['POST'])
def get_duration():
    data = request.get_json()
    if not data or 'file_path' not in data:
        return jsonify({"error": "Missing file_path"}), 400

    relative_path = data['file_path']
    input_file = os.path.join(BASE_DIR, relative_path)

    if not os.path.exists(input_file):
        return jsonify({"error": f"File not found: {input_file}"}), 404

    # La commande ffprobe pour obtenir la durée en secondes
    command = [
        'ffprobe',
        '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        input_file
    ]

    try:
        # On exécute la commande et on récupère la sortie
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        duration = float(result.stdout.strip())
        return jsonify({"duration_seconds": duration}), 200
    except (subprocess.CalledProcessError, ValueError) as e:
        return jsonify({"error": "Failed to get duration", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
