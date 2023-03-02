import socket
import threading
from tkinter import *
import tkinter 
from tkinter import simpledialog

HOST = '127.0.0.1'
PORT =  55555

class Chat:
    def __init__(self):
        
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))

        # Inicialização da interface gráfica do usuário
        login = Tk()
        login.withdraw()
        self.janela_carregada = False
        self.ativo = True

        # Diálogo para inserir o nome do usuário
        self.nome = simpledialog.askstring('Nome', 'Digite seu nome!', parent=login)

        # Diálogo para inserir o nome da sala que o usuário deseja entrar
        self.sala = simpledialog.askstring('Sala', 'Digite a sala que deseja entrar!', parent=login)

        # Thread para lidar com as mensagens recebidas do servidor
        thread = threading.Thread(target=self.conecta)
        thread.start()

        # Inicialização da janela principal
        self.janela()
      
    def janela(self):
        self.root = Tk()
        self.root.geometry("800x800")
        self.root.title('Chat')

        # Área de texto para exibição das mensagens
        self.caixa_texto = Text(self.root)
        self.caixa_texto.place(relx=0.05, rely=0.01, width=700, height=600)

        # Caixa de entrada de texto para envio de mensagens
        self.enviar_mensagem = Entry(self.root)
        self.enviar_mensagem.place(relx=0.05, rely=0.9, width=500, height=30)

        # Botão para enviar a mensagem digitada
        self.btn_enviar = Button(self.root, text='Enviar', command=self.enviarMensagem)
        self.btn_enviar.place(relx=0.8, rely=0.9, width=100, height=30)

        # Configuração para fechar a janela ao clicar no botão 'X'
        self.root.protocol("WM_DELETE_WINDOW", self.fechar)
        self.root.mainloop()


    def conecta(self):
        while True:
            # Recebe uma mensagem do servidor
            recebido = self.client.recv(1024)

            # Se a mensagem for 'b SALA', o cliente envia o nome da sala e o nome do usuário ao servidor
            if recebido == b'SALA':
                self.client.send(self.sala.encode())
                self.client.send(self.nome.encode())

            # Caso contrário, a mensagem é exibida na área de texto
            else:
                try:
                    self.caixa_texto.insert('end', recebido.decode())
                except:
                    pass
            

    
    def fechar(self):
        # Fecha a janela principal e encerra a conexão com o servidor
        self.root.destroy()
        self.client.close()
       

    def enviarMensagem(self):
        # Envia a mensagem digitada para o servidor
        mensagem = self.enviar_mensagem.get()
        self.client.send(mensagem.encode())
        self.enviar_mensagem.delete(0, 'end') # Limpa o campo de mensagem após o envio

# Cria uma instância da classe Chat
chat = Chat()
