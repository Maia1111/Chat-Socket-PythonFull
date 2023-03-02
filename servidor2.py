import socket
import threading

HOST = '127.0.0.1'
PORT = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))

server.listen()

# Dicionário para armazenar as salas e seus clientes
salas = {}

def broadcast(sala, mensagem):
    """
    Envia uma mensagem para todos os clientes na sala especificada.

    :param sala: Sala em que a mensagem será enviada.
    :param mensagem: Mensagem a ser enviada.
    """

    for i in salas[sala]:
        if isinstance(mensagem, str):
            mensagem = mensagem.encode()

        i.send(mensagem + b'\n')

def enviarMensagem(nome, sala, client):
    """
    Recebe mensagens de um cliente e as envia para todos os outros clientes na mesma sala.

    :param nome: Nome do cliente.
    :param sala: Sala em que o cliente está.
    :param client: Objeto socket do cliente.
    """

    while True:
        mensagem = client.recv(104)
        mensagem = f'{nome}: {mensagem.decode()}'
        broadcast(sala, mensagem)


while True:
    # Espera por novas conexões de clientes
    client, addr = server.accept()

    # Envio do nome da sala para o cliente
    client.send(b'SALA')
    sala = client.recv(1024).decode()

    # Envio do nome do cliente para o cliente
    client.send(b'NOME')
    nome = client.recv(1024).decode()

    # Adiciona o cliente na sala apropriada
    if sala not in salas.keys():
        salas[sala] = []
    salas[sala].append(client)

    print(f'{nome} se conectou na sala {sala}! INFO {addr}')

    # Notifica os outros clientes que um novo cliente entrou na sala
    broadcast(sala, f'{nome}: Entrou na sala!')

    # Inicia uma nova thread para lidar com as mensagens do cliente
    thread = threading.Thread(target=enviarMensagem, args=(nome, sala, client))
    thread.start()
