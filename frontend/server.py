from flask import Flask, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/index.html')
@app.route('/')
def serve_react_app():
    return send_from_directory('dist', 'index.html')

@app.route('/assets/<path:path>')
def serve_assets(path):
    return send_from_directory('dist/assets', path)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
