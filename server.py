import os

from dotenv import load_dotenv
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

load_dotenv()

# definindo a porta do servidor FTP
FTP_PORT = int(os.getenv("FTP_PORT", 21))
FTP_ADDR = "0.0.0.0"  # escutando em todas as interfaces
configs = {
    "username": os.getenv("FTP_USER", "user"),
    "password": os.getenv("FTP_PASS", "12345"),
    "homedir": os.getenv("FTP_HOME", "/home/user"),
    "perm": "elradfmw",  # e = listar, l = listar detalhe, r = ler, a = append, d = deletar, f = renomear, m = mkdir, w = escrever
}
# autorizações
authorizer = DummyAuthorizer()
authorizer.add_user(**configs)
# manipulador do FTP
ftp_handler = FTPHandler
ftp_handler.passive_ports = range(60000, 65535)
ftp_handler.authorizer = authorizer

# criando o servidor FTP
server = FTPServer((FTP_ADDR, FTP_PORT), ftp_handler)

# iniciando o servidor FTP
server.serve_forever()
