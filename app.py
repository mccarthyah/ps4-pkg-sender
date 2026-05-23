from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import requests

PKG_DIR = "/app/pkg"
PS4_IP = "10.10.10.57"
PORT = 58880

app = Flask(__name__)

# --- recursively find all PKGs ---
def list_pkgs():
    pkgs = []
    for root, _, files in os.walk(PKG_DIR):
        for f in files:
            if f.endswith(".pkg"):
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, PKG_DIR)
                pkgs.append(rel_path.replace("\\", "/"))
    return sorted(pkgs)

@app.route("/")
def index():
    return render_template("index.html", files=list_pkgs(), ps4_ip=PS4_IP)

@app.route("/pkg/<path:filename>")
def serve_pkg(filename):
    return send_from_directory(PKG_DIR, filename, as_attachment=False)

@app.route("/install/<path:filename>", methods=["POST"])
def install(filename):
    url = f"http://10.10.10.42:{PORT}/pkg/{filename}"
    api = f"http://{PS4_IP}:12800/api/install"

    payload = {
        "type": "direct",
        "packages": [url]
    }

    try:
        r = requests.post(api, json=payload, timeout=5)
        return jsonify({"ok": True, "response": r.text})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
