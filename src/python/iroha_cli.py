from iroha import Iroha, IrohaGrpc, IrohaCrypto as crypto
from iroha import primitive_pb2 , qry_responses_pb2
from iroha import qry_responses_pb2
import schema
#from schema/primitive.proto import RolePermission
import sys
from google.protobuf.pyext import _message 
from protobuf_to_dict import protobuf_to_dict
import json

sys.path.insert(1, '/home/gabriel/Documentos/iroha1/iroha-iroha1-main/example')

# Configurar la conexión al nodo Iroha
network_address = 'localhost:50051'  # Cambiar según la configuración de tu nodo
admin_private_key_path = sys.path[1]+ '/admin@test.priv'
admin_public_key_path = sys.path[1] + '/admin@test.pub'


# Leer la clave privada del archivo
with open(admin_private_key_path, 'r') as f:
 admin_private_key = f.read().strip()

# Leer la clave pública del archivo
with open(admin_public_key_path, 'r') as f:
 admin_public_key = f.read().strip()

iroha = Iroha('admin@test')
net = IrohaGrpc(network_address)


#   Función para obtener nombre de error a partir de codigo
def obtener_nombre_error(reason):
    try:
        nombre_error = qry_responses_pb2.ErrorResponse.Reason.Name(reason)
    except ValueError:
        nombre_error = f"Reason {reason} desconocido"
    return nombre_error


# Obtener el hash de la transacción firmada
def obtener_hash(signed_tx):
    tx_hash = crypto.hash(signed_tx)
    # Convertir el hash a formato hexadecimal
    tx_hash_hex = tx_hash.hex()
    return tx_hash_hex


# endpoint validos

#   1. Crear un nuevo activo 
#   Función para crear un nuevo activo
def create_asset(asset_name, domain_id, precision):
    create_asset_tx = iroha.transaction([
        iroha.command('CreateAsset', asset_name=asset_name, domain_id=domain_id, precision=precision)
    ])

    signed_tx = crypto.sign_transaction(create_asset_tx, admin_private_key)
    net.send_tx(signed_tx)
    status = net.tx_status(signed_tx)

    return {'responseContent': status ,'transactionHash': obtener_hash(signed_tx) }    
    #return obtener_hash(signed_tx),status

#   2. Añadir cantidad a un activo existente ")
#   Función para añadir cantidad a un activo existente
def add_asset_quantity(asset_name, domain_id, amount ):
    add_asset_quantity_tx = iroha.transaction([
        iroha.command('AddAssetQuantity', asset_id=f'{asset_name}#{domain_id}', amount=amount)
    ])
    signed_tx = crypto.sign_transaction(add_asset_quantity_tx, admin_private_key)
    net.send_tx(signed_tx)
    status = net.tx_status(signed_tx)
    
    return obtener_hash(signed_tx),status

#   2.1. Substraer cantidad a un activo existente ")
#   Función para añadir cantidad a un activo existente
def subtract_asset_quantity(asset_name, domain_id, amount ):
    add_asset_quantity_tx = iroha.transaction([
        iroha.command('SubtractAssetQuantity', asset_id=f'{asset_name}#{domain_id}', amount=amount)
    ])
    signed_tx = crypto.sign_transaction(add_asset_quantity_tx, admin_private_key)
    net.send_tx(signed_tx)
    status = net.tx_status(signed_tx)
    
    return obtener_hash(signed_tx),status



#   3. Tranferir de una cuenta a otra
#   Función para transferir una cantidad de una asset de un usurio a otro
def transfer_asset(source_account, destination_account, asset_name, amount):
    domain_destination = destination_account.split('@')[1]
    
    tranfer_asset_quantity_tx = iroha.transaction([
        iroha.command('TransferAsset', src_account_id=source_account,
                      dest_account_id=destination_account, asset_id=f'{asset_name}#{domain_destination}',
                      description='init top up', amount=amount)
    ])
    
    signed_tx = crypto.sign_transaction(tranfer_asset_quantity_tx, admin_private_key)
    net.send_tx(signed_tx)
    tx_hash_hex = obtener_hash(signed_tx)
    status = net.tx_status(signed_tx)

    return tx_hash_hex, status

#   4. Consultar assets de una cuenta (pronto)")        
#   Listar activos de una cuenta dada
def get_account_assets(account_id):
    # account_id = input("Ingrese el id de la cuenta a consultar : ")
    query = iroha.query('GetAccountAssets', account_id=account_id)
    crypto.sign_query(query, admin_private_key)

    response = net.send_query(query)
    data = response.account_assets_response.account_assets
    lista = []
    for asset in data:
        dict = {}
        dict['asset_id'] = asset.asset_id
        dict['balance'] = asset.balance
        lista.append(dict)
    
    return len(lista),lista
    #for asset in data:
     #   print(f'Asset id = {asset.asset_id}, balance = {asset.balance}')

# 5. Consultar todos los permisos relacionado a un rol (get_role_perm)")
def get_role_perm(rol_select):
    #get_roles();
    #rol_select= input("Ingrese un rol de los anteriores listados: ")
    query = iroha.query('GetRolePermissions',counter=2 ,role_id=rol_select)
    crypto.sign_query(query, admin_private_key)

    response = net.send_query(query)
    permisos = response.role_permissions_response.permissions
    lista = []
    for permiso in permisos:
        lista.append(primitive_pb2.RolePermission.Name(permiso))
    
    return rol_select, len(lista), lista
    

# 6. Consultar transacciones de una cuenta (get_acc_transaccion)
def get_acc_transaccion(account_id):
    query = iroha.query('GetAccountTransactions', account_id=account_id, page_size=100)
    crypto.sign_query(query, admin_private_key)

    response = net.send_query(query)
    print(response)
    data = response.transactions_page_response.transactions
    lista = []
    for transaction in data:
        transaction_details = {
            'creator_account_id': transaction.payload.reduced_payload.creator_account_id,
            'created_time': transaction.payload.reduced_payload.created_time,
            'quorum': transaction.payload.reduced_payload.quorum
        }
        commands = []
        commandos = transaction.payload.reduced_payload.commands
        for command in commandos:
            command_type = command.WhichOneof('command')
                  
            if command_type == 'add_asset_quantity':
                add_asset_command = command.add_asset_quantity
                command_details = {
                    'command_type': 'add_asset_quantity',
                    'asset_id': add_asset_command.asset_id,
                    'amount': add_asset_command.amount
                }
            elif command_type == 'create_asset':
                create_asset_command = command.create_asset
                command_details = {
                    'command_type': 'create_asset',
                    'asset_name': create_asset_command.asset_name,
                    'domain_id': create_asset_command.domain_id,
                    'precision': create_asset_command.precision
                }
            elif command_type == 'set_account_quorum':
                set_quorum_command = command.set_account_quorum
                command_details = {
                    'command_type': 'set_account_quorum',
                    'account_id': set_quorum_command.account_id,
                    'quorum': set_quorum_command.quorum
                }
            elif command_type == 'subtract_asset_quantity':
                subtract_asset_command = command.subtract_asset_quantity
                command_details = {
                    'command_type': 'subtract_asset_quantity',
                    'asset_id': subtract_asset_command.asset_id,
                    'amount': subtract_asset_command.amount
                }
            elif command_type == 'add_peer':
                add_peer_command = command.add_peer
                command_details = {
                    'command_type': 'add_peer',
                    'peer_address': add_peer_command.peer.address,
                    'peer_public_key': add_peer_command.peer.peer_key
                }            
            elif command_type == 'remove_peer':
                remove_peer_command = command.remove_peer
                command_details = {
                    'command_type': 'remove_peer',
                    'peer_public_key': remove_peer_command.peer_key
                }
            elif command_type == 'grant_permission':
                grant_permission_command = command.grant_permission
                command_details = {
                    'command_type': 'grant_permission',
                    'account_id': grant_permission_command.account_id,
                    'permission': grant_permission_command.permission
                }
            elif command_type == 'revoke_permission':
                revoke_permission_command = command.revoke_permission
                command_details = {
                    'command_type': 'revoke_permission',
                    'account_id': revoke_permission_command.account_id,
                    'permission': revoke_permission_command.permission
                }
            elif command_type == 'transfer_asset':
                transfer_asset_command = command.transfer_asset
                command_details = {
                    'command_type': 'transfer_asset',
                    'src_account_id': transfer_asset_command.src_account_id,
                    'dest_account_id': transfer_asset_command.dest_account_id,
                    'asset_id': transfer_asset_command.asset_id,
                    'description': transfer_asset_command.description
                }
            elif command_type == 'subtract_peer':
                subtract_peer_command = command.subtract_peer
                command_details = {
                    'command_type': 'subtract_peer',
                    'peer_public_key': subtract_peer_command.peer_key
                }
            elif command_type == 'set_account_detail':
                set_account_detail_command = command.set_account_detail
                command_details = {
                    'command_type': 'set_account_detail',
                    'account_id': set_account_detail_command.account_id,
                    'key': set_account_detail_command.key,
                    'value': set_account_detail_command.value
                }
            elif command_type == 'remove_signatory':
                remove_signatory_command = command.remove_signatory
                command_details = {
                    'command_type': 'remove_signatory',
                    'account_id': remove_signatory_command.account_id,
                    'public_key': remove_signatory_command.public_key
                }
            elif command_type == 'set_quorum':
                set_quorum_command = command.set_quorum
                command_details = {
                    'command_type': 'set_quorum',
                    'account_id': set_quorum_command.account_id,
                    'quorum': set_quorum_command.quorum
                }
            elif command_type == 'add_signatory':
                add_signatory_command = command.add_signatory
                command_details = {
                    'command_type': 'add_signatory',
                    'account_id': add_signatory_command.account_id,
                    'public_key': add_signatory_command.public_key
                }

            # Añadir más bloques `elif` para otros tipos de comandos como `transfer_asset`, etc.
            else:
                # Manejar cualquier otro tipo de comando o casos no esperados
                command_details = {
                    'command_type': command_type,
                    'details': 'No se ha implementado el manejo para este tipo de comando'
                }
            
            commands.append(command_details)
        transaction_details['total_commands'] = len(commands)
        transaction_details['commands_list'] = commands
        lista.append(transaction_details)
            #lista.append({
              #  'command_type': command_type,
               # 'command_details': command.__getattribute__(command_type) if command_type else None
           # })
    
    return {'total_transactions': len(lista), 'transactions_list': lista}


#  7. Consultar todos los roles en el sistema (get_roles)(pronto)
def get_roles():
    query = iroha.query('GetRoles')
    crypto.sign_query(query, admin_private_key)
    response = net.send_query(query)
    roles = response.roles_response.roles
    lista = []
    for rol in roles:
            lista.append(rol)
    
    return len(lista), lista

#   8. Consultar informacion acerca de un asset (get_ast_info)(pronto)")
#   Informacion de un asset determinado
def get_ast_info(asset_name):
    query = iroha.query('GetAssetInfo', asset_id=asset_name)
    crypto.sign_query(query, admin_private_key)

    response = net.send_query(query)
    data = response.asset_response.asset
    elJson = {'assetName': data.asset_id , 'precision': data.precision } 
    
    return elJson

#   9. Consultar informacion acerca de una transaccion a partir de hash
#   Informacion de un asset determinado
def get_transaction_status(tx_hash_a_consultar):
    tx_hash1 = {tx_hash_a_consultar}  # Utiliza el hash recibido como parámetro
    query = iroha.query('get_transactions', tx_hashes={tx_hash_a_consultar})
    
    crypto.sign_query(query, admin_private_key)
    response = net.send_query(query)
    print(response)

    response_dict = protobuf_to_dict(response)
    
    if 'error_response' in response_dict:
        error_message = response_dict['error_response']['message']
        error_code = response_dict['error_response']['error_code']
        status = f"Error: {error_message} (Error code: {error_code})"
        reason = response_dict['error_response']['reason']
        response_dict['error_response']['reason'] = obtener_nombre_error(reason)
        error_code_num = response_dict['error_response'].get('error_code', None)
        print('afadfadf')
        #print(error_code_num)
        #error_code_name = qry_responses_pb2.ErrorResponse.ErrorCode.Name(error_code_num)
        print('afadfadf')
        #print(error_code_name)
        #response_dict['error_response']['error_code'] = error_code_name
    else:
        status = "Transacción exitosa"

    # Obtener el hash de la consulta 
    query_hash = response_dict.pop('query_hash', None)
        
    # Serializar el diccionario a formato JSON
    serialized_json = json.dumps(response_dict, indent=4)
    # Imprimir la cadena JSON serializada
    print(serialized_json)

    ordered_response = {
        'status': status,
        'query_hash': query_hash,
        'response_content': response_dict
    }
    return ordered_response
