from flask import Flask, send_from_directory

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    print("🌐 WEB SERVER Flask pronto sulla porta 5000")
    app.run(debug=True, port=5000, host='0.0.0.0')

