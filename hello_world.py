import time
import base64
from cryptography.fernet import Fernet

def descriptografar(dados_criptografados, chave):
    """Descriptografa os dados criptografados usando a chave fornecida."""
    f = Fernet(chave)
    dados_descriptografados = f.decrypt(dados_criptografados).decode()
    return dados_descriptografados

def desembaralhar(dados_embaralhados):
    """Desembaralha os dados embaralhados."""
    dados_desembaralhados = base64.b64decode(dados_embaralhados)
    return dados_desembaralhados

def ler_licenca(arquivo_licenca="licenca.bin"):
    """Lê o arquivo de licença e retorna o tempo limite."""
    try:
        with open(arquivo_licenca, "rb") as f:
            conteudo = f.read()
            chave, dados_embaralhados = conteudo.split(b"|", 1)
            dados_desembaralhados = desembaralhar(dados_embaralhados)
            dados_descriptografados = descriptografar(dados_desembaralhados, chave)
            tempo_limite = int(dados_descriptografados)
            return tempo_limite
    except FileNotFoundError:
        return None

def hello_world(arquivo_licenca="licenca.bin"):
    """Imprime "Hello, World!" com uma licença de tempo limitado."""
    tempo_limite = ler_licenca(arquivo_licenca)

    if tempo_limite is None:
        print("Arquivo de licença não encontrado.")
        return

    tempo_inicial = time.time()
    tempo_final = tempo_inicial + tempo_limite

    while time.time() < tempo_final:
        print("Hello, World!")
        time.sleep(1)

    print("Licença expirada. O programa não está mais disponível.")

if __name__ == "__main__":
    hello_world()