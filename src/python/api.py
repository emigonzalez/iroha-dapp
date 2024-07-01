from flask import Flask, request
from flask import jsonify
import sys
from config import config
from google.protobuf.json_format import MessageToJson
from google.protobuf.json_format import MessageToDict
import json
from protobuf_to_dict import protobuf_to_dict

sys.path.insert(1, '/home/gabriel/Documentos/iroha1/iroha-iroha1-main/example')

import iroha_cli


def create_app(enviroment):
    app = Flask(__name__)

    app.config.from_object(enviroment)

    return app

enviroment = config['development']
app = create_app(enviroment)

#   1. Crear un nuevo activo 
@app.route('/api/v1/assets/', methods=['POST'])
def create_asset():
    json = request.get_json(force=True)

    if json.get('assetName') is None or json.get('domainId') is None or json.get('precision') is None:
        return jsonify({'message': 'Bad request'}), 400

    response = iroha_cli.create_asset(json['assetName'], json['domainId'], json['precision'])
    return jsonify(response)


#   2. Añadir cantidad a un activo existente ")
@app.route('/api/v1/assets/add_quantity', methods=['POST'])
def add_asset_quantity():
    body = request.get_json(force=True)

    if body.get('assetName') is None or body.get('domainId') is None or body.get('amount') is None:
        return jsonify({'message': 'Bad request'}), 400
    response = iroha_cli.add_asset_quantity(body['assetName'], body['domainId'], body['amount'])
    r = json.dumps(response)
    return r

#   2.1 Substraer cantidad a un activo existente ")
@app.route('/api/v1/assets/subtract_quantity', methods=['POST'])
def subtract_asset_quantity():
    body = request.get_json(force=True)

    if body.get('assetName') is None or body.get('domainId') is None or body.get('amount') is None:
        return jsonify({'message': 'Bad request'}), 400
    response = iroha_cli.subtract_asset_quantity(body['assetName'], body['domainId'], body['amount'])
    r = json.dumps(response)
    return r



#   3. Tranferir de una cuenta a otra
@app.route('/api/v1/assets/tranfer', methods=['POST'])
def transfer_asset():
    body = request.get_json(force=True)

    if body.get('sourceAccount') is None or body.get('destinationAccount') is None or body.get('assetName') is None or body.get('amount') is None:
        return jsonify({'message': 'Bad request'}), 400
    
    response = iroha_cli.transfer_asset(body['sourceAccount'], body['destinationAccount'], 
                                        body['assetName'], body['amount'])
    elJson= json.dumps(response)
    return elJson

#   4. Consultar assets de una cuenta 
@app.route('/api/v1/assets/<accountId>', methods=['GET'])
def get_assets(accountId):
    response = iroha_cli.get_account_assets(accountId)
    r = json.dumps(response)
    return r

#   5. Consultar todos los permisos relacionado a un rol 
@app.route('/api/v1/rol/<rolId>', methods=['GET'])
def get_role_perm(rolId):
    response = iroha_cli.get_role_perm(rolId)
    r = json.dumps(response)
    return r

# 6. Consultar transacciones de una cuenta (get_acc_transaccion)
@app.route('/api/v1/account/transactions/<accountId>', methods=['GET'])
def get_acc_transaccion(accountId):
    response = iroha_cli.get_acc_transaccion(accountId)
    r = json.dumps(response)
    return r

#  7. Consultar todos los roles en el sistema (get_roles)(pronto)
@app.route('/api/v1/rol', methods=['GET'])
def get_roles():
    response = iroha_cli.get_roles()
    r = json.dumps(response)
    return r


#   8. Consultar informacion acerca de un asset 
@app.route('/api/v1/assets/info/<assetName>', methods=['GET'])
def get_ast_info(assetName):
    response = iroha_cli.get_ast_info(assetName)
    r = json.dumps(response)
    return r


#   9. Consultar informacion acerca de una trasaccion 
@app.route('/api/v1/transactions/info/<transactionsHash>', methods=['GET'])
def get_transaction_status(transactionsHash):
    response = iroha_cli.get_transaction_status(transactionsHash)
    r = json.dumps(response)
    return r


# app.route('/api/v1/asset_name, domain_id, precisionusers', methods=['GET'])
# def get_users():
#     response = {'message': 'success'}
#     return jsonify(response)

# @app.route('/api/v1/users/<id>', methods=['PUT'])
# def update_user(id):
#     response = {'message': 'success'}
#     return jsonify(response)

# @app.route('/api/v1/users/<id>', methods=['DELETE'])
# def delete_user(id):
#     response = {'message': 'success'}
#     return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)