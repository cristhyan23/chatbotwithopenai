import base64
import os
from openai import OpenAI
from dotenv import load_dotenv

"""Classe mae responsavel por add integração com a openai salvar e carregar os arquivos para direcionar ao app.py e selecipna persona"""
class Helpers:

    def __init__(self):
        #faz inicialização da api e modelo do chatbot
        self.obj = self.inicializa_gpt()
        #mapeia qual o caminho esta salvo todo o programa
        self.caminho_pasta = os.path.abspath(os.path.dirname(__file__))

    #função que inicializa o modelo do chatbot
    def inicializa_gpt(self):
        load_dotenv()
        self.cliente = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.modelo = "gpt-4-1106-preview"

#função que faz leitura dos arquivos base para o chatbot
    def carrega(self,caminho_arquivo):
        try:
            with open(caminho_arquivo,"r",encoding="utf-8") as arquivo:
            # Extrai o texto 
                texto = arquivo.read()
                return texto
        except IOError as e:
            print(f"Error {e}")

#função pra salvar os textos gerados pelo chatbot
    def salva_arquivo(self,nome_do_arquivo,conteudo):
        try:
            with open(nome_do_arquivo,"w",encoding="utf-8") as arquivo:
                arquivo.write(conteudo)
        except IOError as e:
            print(f'Erro ao salvar o arquivo: {e}')

# função para transformar imagens em prompts
    def encodar_imagem(self, url):
        with open(url, "rb") as arquivo_imagem:
            return base64.b64encode(arquivo_imagem.read()).decode('utf-8')