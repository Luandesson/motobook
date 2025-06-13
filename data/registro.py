# Importa o módulo 'json', que permite salvar e carrregar dados em arquivos .json
import json

# Importa o módulo 'os', que permite interagir com o sistema operacional (como caminho de arquivos)
import os

# Definir o nome da pasta onde os arquivos serão salvos
DATA_FOLDER = "data"

# Definir o caminho completo onde o arquivo de abastecimento será salvo
ABASTECIMENTOS_FILE = os.path.join(DATA_FOLDER, "ABASTECIMENTOS.json")

# Definir o caminho completo onde o arquivo de trocas de óleo será salvo
OLEO_FILE   = os.path.join(DATA_FOLDER, "oleo.json")

#----------------------------------------
# Função qque SALVA uma lista de dados em arquvi .json
#----------------------------------------------
def salvar_json(dados, caminho):
    # Abre o arquivo no modo de escrita ("W") e com codificação UTF-8
    with open(caminho, "w", encoding="utf-8") as f:
        # Converte a lista de dados em JSON e escreve no arquivo
        json.dump(dados, f, ensure_ascii=False, indent=4)

#-----------------------------------
# Função que CARREGA uma lista de dados de um arquivo .json
#-----------------------------------
def carregar_json(caminho):
    # Se o arquivo ainda não existir, retorna uma lista vazia
    if not os.path.exists(caminho):
        return []
    
    # Se o arquivo existir, abre ele no modo de Leitura ("r")
    with open(caminho, "r", encoding="utf-8") as f:
        # Lê o conteúdo do arquivo e converte de volta para lista PYTHON
        return json.load(f)