import time
import base64
from cryptography.fernet import Fernet
from argparse import ArgumentParser

print('''
usage: license_generator.py [option] ... [-h horas | -m minutos | -s segundos] [arg] ...
    Options:
-h --horas   : Quantidade de horas para validade da licença. Valor padrão é 4 horas.
-d --dias    : Quantidade de dias para validade da licença
''')

parser = ArgumentParser()
parser.add_argument("--h", "--horas", dest="horas",
                    help="Quantidade de horas para validade da licença", metavar="HORAS")

parser.add_argument("-d", "--dias", dest="dias",
                    help="Quantidade de dias para validade da licença", metavar="DIAS")


def gerar_chave():
    """Gera uma chave de criptografia Fernet."""
    chave = Fernet.generate_key()
    return chave

def criptografar(dados, chave):
    """Criptografa os dados usando a chave fornecida."""
    f = Fernet(chave)
    dados_criptografados = f.encrypt(dados.encode())
    return dados_criptografados

def embaralhar(dados):
    """Embaralha os dados."""
    dados_embaralhados = base64.b64encode(dados).decode()
    return dados_embaralhados

def gerar_licenca(tempo_limite, arquivo_licenca="licenca.bin"):
    """Gera um arquivo de licença criptografado e embaralhado."""
    chave = gerar_chave()
    dados = str(tempo_limite)
    dados_criptografados = criptografar(dados, chave)
    dados_embaralhados = embaralhar(dados_criptografados)

    with open(arquivo_licenca, "wb") as f:
        f.write(chave + b"|" + dados_embaralhados.encode())

args = parser.parse_args()
horas = args.horas
dias = args.dias

if horas:
    horas = int(args.horas) 
else:
    horas = 0

if dias:
    dias = int(args.dias)
else:
    dias = 0

tempo_limite = ((dias*24+horas)*60)*60

if __name__ == "__main__":
    gerar_licenca(tempo_limite)
    print(f"Arquivo de licença '{arquivo_licenca}' gerado com sucesso.")
