from flask import Flask, jsonify, request, send_file
import os
from pathlib import Path

app = Flask(__name__)
PKG_DIR = Path('/app/pkgs')
PKG_DIR.mkdir(exist_ok=True)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'ps4-pkg-sender'}), 200

@app.route('/list', methods=['GET'])
def list_pkgs():
    pkgs = [f.name for f in PKG_DIR.glob('*.pkg')]
    return jsonify({'pkgs': pkgs, 'count': len(pkgs)}), 200

@app.route('/pkgs/<filename>', methods=['GET'])
def download_pkg(filename):
    file_path = PKG_DIR / filename
    if not file_path.exists() or not file_path.suffix == '.pkg':
        return jsonify({'error': 'File not found'}), 404
    return send_file(file_path, as_attachment=True)

@app.route('/upload', methods=['POST'])
def upload_pkg():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.endswith('.pkg'):
        return jsonify({'error': 'Only .pkg files allowed'}), 400
    
    file.save(PKG_DIR / file.filename)
    return jsonify({'message': 'File uploaded successfully', 'filename': file.filename}), 201

@app.route('/info', methods=['GET'])
def info():
    return jsonify({
        'service': 'PS4 PKG Sender',
        'version': '1.0.0',
        'server_ip': '10.10.10.57',
        'server_port': 58880,
        'ps4_ip': '10.10.10.120'
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
