import os
import time
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
if not os.path.exists(LOCAL_DIR):
    os.makedirs(LOCAL_DIR)

# pasta no servidor FTP para navegar
REMOTE_DIR = os.getenv("FTP_DIR", "uploads")
print(f"""Configurações do FTP:
HOSTNAME: {configs["host"]},
PORT: {configs["port"]},
USER: {configs["user"]},
PASSWD: {configs["passwd"]},
LOCAL_DIR: {LOCAL_DIR},
REMOTE_DIR: {REMOTE_DIR}
      """)

# instanciando o cliente FTP
ftp = FTP()
# nível de debug (0 = sem debug, 1 = básico, 2 = detalhado)
ftp.set_debuglevel(2)
# conectando ao servidor FTP
ftp.connect(configs["host"], configs["port"], timeout=60)
print(f"Conectado ao servidor FTP {configs['host']} na porta {configs['port']}")
# fazendo login
ftp.login(configs["user"], configs["passwd"])
print(f"Logado como {configs['user']}")

# navegando até a pasta desejada
ftp.cwd(REMOTE_DIR)
print(f"Diretório atual: {ftp.pwd()}")
print(f"Navegando até a pasta {REMOTE_DIR}")


def main():
    mode = False
    # listando os arquivos na pasta remota
    while True:
        mode = not mode
        # Configurando para modo passivo (importante para contornar firewalls/NAT)
        ftp.set_pasv(mode)
        print(f"Modo passivo {mode} ativado")
        try:
            files = ftp.nlst()
            print("Listagem de arquivos realizada com sucesso.")
            break
        except Exception as e:
            print(f"Erro ao listar arquivos: {e}")
            files = []

    files_success = 0
    print(f"Arquivos na pasta {REMOTE_DIR}: {len(files)}")
    for file in files:
        while True:
            mode = not mode
            # Configurando para modo passivo (importante para contornar firewalls/NAT)
            ftp.set_pasv(mode)
            print(f"Modo passivo {mode} ativado")
            try:
                local_filepath = os.path.join(LOCAL_DIR, file)
                with open(local_filepath, "wb") as f:
                    # baixando o arquivo
                    ftp.retrbinary(f"RETR {file}", f.write, 8192)
                print(f"Arquivo {file} baixado com sucesso!")
                files_success += 1
                # deletando o arquivo do servidor FTP após o download
                ftp.delete(file)
                print(f"Arquivo {file} deletado do servidor FTP.")
                break
            except Exception as e:
                print(f"Erro ao processar o arquivo {file}: {e}")

    print(f"Total de arquivos baixados com sucesso: {files_success}")
    # fechando a conexão
    ftp.quit()


if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            print(f"[DEBUG] >> Erro na execução do main: {e}")
        time.sleep(60)
