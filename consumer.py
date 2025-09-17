import os
from ftplib import FTP

from dotenv import load_dotenv

load_dotenv()

# configurações do FTP
configs = {
    "host": os.getenv("FTP_HOST", "0.0.0.0"),
    "port": int(os.getenv("FTP_PORT", 21)),
    "user": os.getenv("FTP_USER", "user"),
    "passwd": os.getenv("FTP_PASS", ""),
}

# pasta local para salvar os arquivos baixados
LOCAL_DIR = os.path.join(os.getcwd(), "downloads")
# parta no servidor FTP para navegar
REMOTE_DIR = os.getenv("FTP_DIR", "uploads")
# instanciando o cliente FTP
ftp = FTP()
# conectando ao servidor FTP
ftp.connect(configs["host"], configs["port"])
# fazendo login
ftp.login(configs["user"], configs["passwd"])

# navegando até a pasta desejada
ftp.cwd(LOCAL_DIR)
# listando os arquivos na pasta remota
files = ftp.nlst()

for file in files:
    local_filepath = os.path.join(LOCAL_DIR, file)
    with open(local_filepath, "wb") as f:
        # baixando o arquivo
        ftp.retrbinary(f"RETR {file}", f.write)
    print(f"Arquivo {file} baixado com sucesso!")
    # deletando o arquivo do servidor FTP após o download
    ftp.delete(file)
    print(f"Arquivo {file} deletado do servidor FTP.")

# fechando a conexão
ftp.quit()
