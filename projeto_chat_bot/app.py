from flask import Flask, render_template, request
from time import sleep
from assistente_lumy import AssistenteLumy
from seleciona_persona import TipoPersonas
import json
from vision_lumy import GestorImagem
import uuid
import os

class AppChatBot(AssistenteLumy,TipoPersonas,GestorImagem):
    def __init__(self):
        super().__init__()

        #função que inicializa o assistente e as threads
        self.assistente = self.pegar_json()
        self.threads_id = self.assistente["thread_id"]
        self.assistente_id= self.assistente["assistant_id"]
        self.file_ids = self.assistente["files_ids"]
        self.STATUS_COMPLETED = "completed"
        self.STATUS_REQUIRES_ACTION = "requires_action"
        #variavel que dar caminho da imagem dentro da pasta temporária
        self.caminho_imagem_enviada = None
        self.UPLOAD_FOLDER = 'dados'
        # Faz inicialização do app para criação do front_end
        self.app = Flask(__name__, static_folder='static')
        self.app.secret_key = "alura"
        #define rota de leitura e tratativa das imagens
        @self.app.route('/upload_imagem', methods=["POST"])
        def upload_imagem():
           
            if 'imagem' in request.files:
                #ações para capturar a imagem enviada no chat para salvar em um diretorio temporário para envio do arquivo para
                imagem_enviada = request.files['imagem']
                nome_arquivo = str(uuid.uuid4())+os.path.splitext(imagem_enviada.filename)[1]
                caminho_arquivo = os.path.join(self.UPLOAD_FOLDER,nome_arquivo)
                imagem_enviada.save(caminho_arquivo)
                self.caminho_imagem_enviada = caminho_arquivo
                return 'imagem enviada com sucesso',200
            return 'nenhum arquivo enviado', 400
        
        # Define as rotas de execução do chat
        @self.app.route("/chat", methods=["POST"])
        def chat():
            prompt = request.json['msg']
            #recebe resposta da AI
            resposta = self.bot(prompt)
            # função para devolver a resposta da AI para o front_end do chat bot
            texto_resposta = resposta if isinstance(resposta, str) else resposta.content[0].text.value
            return texto_resposta

        @self.app.route("/")
        def index():
            return render_template("index.html")
    #função criada para iniciar o servidor Flask
    def run(self):
        self.app.run(debug=True)
    #função responsável pela execução do envio dos dados para a openAI e captura da resposta
    def bot(self,prompt):

        maximo_tentativas = 1
        repeticao = 0
        
        while True:
            try:
                #cria o copilador da mensagem do usuário
                personalidade = self.seleciona_persona(prompt)
                self.cliente.beta.threads.messages.create(
                     thread_id=self.threads_id,
                     role="user",
                     content=f"""Assuma, de agora em diante, a personalidade abaixo
                     ignore as personalidades anteriores, lembre-se que seu nome é Lumybot
                     # Persona
                     {personalidade}
                    caso seja none a persona assuma uma personalidade neutra
                     """,
                     file_ids=self.file_ids
                )
                #ação de desenvolvimento e leitura de imagem
                resposta_vision = ""
                if self.caminho_imagem_enviada !=None:
                     resposta_vision = self.analisar_imagem(self.caminho_imagem_enviada)
                     os.remove(self.caminho_imagem_enviada)
                     self.caminho_imagem_enviada = None


                self.cliente.beta.threads.messages.create(
                     thread_id= self.threads_id,
                     role = "user",
                     #adiciona a resposta do vision com o prompt para retorno do chat, se não tiver nada na variavel vision retorna vazio
                     content= resposta_vision+prompt,
                     file_ids=self.file_ids
                )
                #cria campo de execução acionando o assistente
                run = self.cliente.beta.threads.runs.create(
                     thread_id=self.threads_id,
                     assistant_id=self.assistente_id
                )
                
                # linha de repetição para garantir que a execução foi completa e conseguir responder a pergunta
                while run.status != self.STATUS_COMPLETED:
                     run = self.cliente.beta.threads.runs.retrieve(
                          thread_id=self.threads_id,
                          run_id= run.id
                     )
                     #Status da execuçao do Run
                     print(f'Status: {run.status}')
                    #devio responsavel por absorver um comportamento novo ou não se existir a chamada de função
                     if run.status == self.STATUS_REQUIRES_ACTION:
                            tools_acionadas = run.required_action.submit_tool_outputs.tool_calls
                            respostas_tools_acionadas = []
                            for um_tool in tools_acionadas:
                                nome_funcao = um_tool.function.name
                                funcao_escolhida =  self.lista_funcoes[nome_funcao]
                                args = json.loads(um_tool.function.arguments)
                                print(args)
                                resposta_funcao=funcao_escolhida(args)

                                respostas_tools_acionadas.append({
                                    "tool_call_id":um_tool.id,
                                    "output":resposta_funcao
                                })
                            
                            # Envia a saída das ferramentas de execução de volta
                            run = self.cliente.beta.threads.runs.submit_tool_outputs(
                                thread_id=self.threads_id,
                                run_id=run.id,
                                tool_outputs=respostas_tools_acionadas
                            )
                #acessa todas as respostas dentro do histórico para analise e trataiva para melhor resposta ao usuario
                #necessário converter para modelo de lista se não não é possivel acessar a resposta atual
                historico = list(self.cliente.beta.threads.messages.list(thread_id=self.threads_id).data)
                resposta = historico[0]
                #envia resposta para o usuário
                return resposta               
            
            except Exception as erro:
                    repeticao += 1
                    if repeticao >= maximo_tentativas:
                            return "Erro no GPT: %s" % erro
                    print('Erro de comunicação com OpenAI:', erro)
                    sleep(2)
    
if __name__ == "__main__":
    chat = AppChatBot()
    chat.run()
