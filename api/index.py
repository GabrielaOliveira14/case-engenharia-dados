
from flask import Flask, jsonify
import src.constants.querys as querys
from src.utils.handleQueryConsulta import handleQueryConsulta

app = Flask(__name__)


@app.route('/nomes_repetidos/', methods=['GET'])
def totalRepeatedNamesByCountries():
    final_response = []

    query_response = handleQueryConsulta(querys.repeteadNamesByCountries, '../database/data.db')

    for item in query_response:
        final_response.append({
            "pais": item[0],
            "nome": item[1],
            "repeticoes": item[2]
        })

    return jsonify(final_response)


@app.route('/distribuicao_genero/', methods=['GET'])
def genderByCountry():
    final_response = []

    query_response = handleQueryConsulta(querys.genderByCountry, '../database/data.db')

    for item in query_response:
        final_response.append({
            "pais": item[0],
            "masculino": item[1],
            "feminino": item[2]
        })

    return jsonify(final_response)


@app.route('/distribuicao_genero_50_mais/', methods=['GET'])
def genderByCountryWith50YearsOld():
    final_response = []

    query_response = handleQueryConsulta(querys.genderByCountryWith50YearsOld, '../database/data.db')

    for item in query_response:
        final_response.append({
            "pais": item[0],
            "masculino": item[1],
            "feminino": item[2]
        })

    return jsonify(final_response)


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
