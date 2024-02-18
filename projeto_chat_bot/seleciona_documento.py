from helpers import Helpers


class ClassificaDoc(Helpers):
    def __init__(self):
        super().__init__()

#tipos de arquivos dentro da pasta referente a lumy
        self.politica_lumy = self.carrega(f'{self.caminho_pasta}/dados/politicas_lumy.txt')
        self.dados_lumy = self.carrega(f'{self.caminho_pasta}/dados/dados_lumy.txt')
        self.tipos_temas = self.carrega(f'{self.caminho_pasta}/dados/informacoes.txt')

#mapea resposta do openai e devolver o documento correto para criaçao do contexto para o chatbot
    def seleciona_doc(self,resposta_openai):
        if 'politica' in resposta_openai:
            return self.tipos_temas + "\n" + self.politica_lumy
        elif 'dados' in resposta_openai:
            return self.dados_lumy + "\n"+self.politica_lumy
        else:
            return self.tipos_temas

#faz comunicação com a open ai para de acordo com o texto do usuário definir qual melhor doc
    def selecionar_contexto_doc(self,mensagem_usuario):
        prompt_sistema = f"""
            O Lumybot contém 2 documentos principais que detalha difernetes aspectos do negócio

            Documento 1: "\n{self.politica_lumy}"\n"
            Documento 2:  "\n{self.dados_lumy}"\n"
            Documento 3: "\n{self.tipos_temas}"\n"

            Avalie o prompt do usuário e retorne o documento mais indicado para ser usado
            no contexto da resposta. Retorne Politica se for Documento 1, se for dados sobre a Lumybot Documento 2 e se for contexto dos temas
            que o Lumybot atua Documento 3

"""
        response = self.cliente.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": prompt_sistema
                    },
                    {
                        "role": "user",
                        "content": mensagem_usuario
                    }],
                    temperature=1,
                    model = self.modelo)

        contexto = response.choices[0].message.content
        return contexto   
    
