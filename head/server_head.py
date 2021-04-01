import socket

HOST = 'localhost'
PORT = 60000

def test_function(test):
	print('->Mensassagem do cliente: {}'.format(test))
	return '200'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

print('Aguardando conexão do cliente')
conn, ender = s.accept()

print('Conectado em {}'.format(ender))

while True:

    data = conn.recv(2048)
    data = data.decode()

    if data  == 'exit':
    	print('Fechando conexão')
    	conn.close()
    	break
    else:
    	msg = test_function(data)
    	#print('->Mensassagem do cliente: {}'.format(data.decode()))
    	#msg = 'Servidor OK'
    
    	conn.sendall(msg.encode())