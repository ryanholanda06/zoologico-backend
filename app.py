from flask import Flask, jsonify
from flask_cors import CORS
from conector import Database

app = Flask(__name__)
CORS(app) # Libera o acesso para o seu frontend

db = Database()

# Rota de teste só para ver se o servidor tá vivo
@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "Servidor rodando!"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
