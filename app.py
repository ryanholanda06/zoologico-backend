from flask import Flask, request, jsonify
from flask_cors import CORS
from conector import Database

app = Flask(__name__)
CORS(app)  # Permite que o frontend comunique com esta API sem bloqueios de CORS

db = Database()

# Rota 1: Listar livros com filtros dinâmicos por RG do autor, editora ou ISBN
@app.route('/livros', methods=['GET'])
def get_livros():
    rg_autor = request.args.get('rg', '')
    editora_id = request.args.get('editora', '')
    isbn = request.args.get('isbn', '')

    query = """
        SELECT 
            l.isbn, l.titulo, 
            e.nome AS editora, 
            a.nome AS autor, a.rg
        FROM livro l
        LEFT JOIN editora e ON e.id = l.editora_id
        LEFT JOIN escreve es ON es.isbn = l.isbn
        LEFT JOIN autor a ON a.rg = es.rg
        WHERE 1=1
    """
    params = []

    if rg_autor:
        query += " AND a.rg = %s"
        params.append(rg_autor)
    if editora_id:
        query += " AND e.id = %s"
        params.append(editora_id)
    if isbn:
        query += " AND l.isbn = %s"
        params.append(isbn)

    livros = db.execute_select(query, params)
    return jsonify(livros), 200

# Rota 2: Alertar sobre impressões concluídas (data_entrega <= hoje)
@app.route('/impressos', methods=['GET'])
def get_impressos():
    query = """
        SELECT i.id, l.titulo, g.nome AS grafica, i.copias, i.data_entrega
        FROM imprime i
        JOIN livro l ON l.isbn = i.isbn
        JOIN grafica g ON g.id = i.grafica_id
        WHERE i.data_entrega <= CURRENT_DATE
    """
    impressos = db.execute_select(query)
    # Converter datas para texto para enviar no JSON sem erros
    for item in impressos:
        item['data_entrega'] = str(item['data_entrega'])
    return jsonify(impressos), 200

# Rota 3: Requisitar nova impressão de livro (POST)
@app.route('/impressos', methods=['POST'])
def criar_impressao():
    dados = request.get_json()
    isbn = dados.get('isbn')
    grafica_id = dados.get('grafica_id')
    copias = dados.get('copias')
    data_entrega = dados.get('data_entrega')

    query = """
        INSERT INTO imprime (isbn, grafica_id, copias, data_entrega)
        VALUES (%s, %s, %s, %s)
    """
    db.execute_statement(query, (isbn, grafica_id, copias, data_entrega))
    return jsonify({"mensagem": "Impressão requisitada com sucesso!"}), 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)