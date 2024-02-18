import os
import json
from openai import BadRequestError
from tools_lumy import ToolsLumy
class AssistenteLumy(ToolsLumy):
    def __init__(self):
        super().__init__()
           
    def criar_threads(self):
        return self.cliente.beta.threads.create()
    
    def criar_lista_ids(self):
        # atenção o assistente tem capacidade de consumir até 20 arquivos por vez
        lista_ids_arquivos = []    
        # Lista de arquivos a serem criados
        arquivos = ["dados/dados_lumy.txt", "dados/politicas_lumy.txt", "dados/informacoes.txt","dados/promocional.txt"]
        for arquivo_path in arquivos:
            if os.path.exists(arquivo_path):
                with open(arquivo_path, "rb") as arquivo:
                    file_obj = self.cliente.files.create(file=arquivo, purpose='assistants')
                    lista_ids_arquivos.append(file_obj.id)
            else:
                print(f"O arquivo {arquivo_path} não existe.")
        
        return lista_ids_arquivos

    def pegar_json(self):
            file_name = 'assistente_files.json'
            if not os.path.exists(file_name):
                try:
                    thread_id = self.criar_threads()
                    files_id = self.criar_lista_ids()
                    assistant_id = self.criar_assistente(files_id)
                    data = {
                        "assistant_id": assistant_id.id,
                        "thread_id": thread_id.id,
                        "files_ids": files_id
                    }
                    with open(file_name, "w", encoding="utf-8") as file:
                        json.dump(data, file, ensure_ascii=False, indent=4)
                        print("Arquivo JSON criado com sucesso")
                    return data
                except BadRequestError as e:
                    print(f"Erro ao criar assistente: {e}")
            else:
                try:
                        with open(file_name, 'r', encoding="utf-8") as file:
                            data = json.load(file)
                            return data
                except FileNotFoundError:
                        print("Arquivo não encontrado")
                

    def criar_assistente(self,files_id):
        assistente = self.cliente.beta.assistants.create(
            name = "Lumy",
            instructions= f"""
                Você é um assistente virtual que tem o nome de Lumybot, especializado em beleza, pronto para fornecer dicas e conselhos sobre cuidados com a pele, maquiagem, cabelo, estilo e bem-estar.
                Configuração Inicial: Você deve ser capaz de responder a perguntas sobre os tópicos listados abaixo, no contexto atual.
               Além disso, acesse os arquivos associados a você e a thread para responder as perguntas   
               caso não tenha arquivos atue de maneira positiva e alegre
               Também pode validar codigos promocionais da Lumy   
            """,
            model=self.modelo,
            tools=self.tools,
            file_ids=files_id
        )

        return assistente

