from flask import Flask, render_template, request, jsonify
from despesas import adicionar_despesa, listar_despesas, atualizar_despesa, remover_despesa
import os


app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/despesas', methods=['GET'])
def get_despesas():
    return jsonify(listar_despesas())


@app.route('/despesas', methods=['POST'])
def post_despesa():
    dados = request.get_json()
    if not isinstance(dados["valor"], (int, float)):
        return jsonify({"erro": "Valor inválido"}), 400
    elif dados["valor"] < 0:
        dados["valor"] = dados["valor"] * -1
        return post_despesa()
    else:
        despesa = adicionar_despesa(dados["descricao"], dados["valor"], dados["categoria"])
        return jsonify(despesa), 201


@app.route('/despesas/<int:id>', methods=['PUT'])
def put_despesa(id):
  dados = request.get_json()
  despesa = atualizar_despesa(id, dados.get("descricao"), dados.get("valor"), dados.get("categoria"))
  if despesa:
      return jsonify(despesa)
  return jsonify({"erro": "Despesa não encontrada"}), 404


@app.route('/despesas/<int:id>', methods=['DELETE'])
def delete_despesa(id):
  if remover_despesa(id):
      return jsonify({"mensagem": "Despesa removida com sucesso"})
  return jsonify({"erro": "Despesa não encontrada"}), 404


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Render passa a porta em $PORT
    app.run(host="0.0.0.0", port=port)

