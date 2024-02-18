from helpers import Helpers

class GestorImagem(Helpers):
    def __init__(self):
        super().__init__()
        self.modelo =  "gpt-4-vision-preview"

    def analisar_imagem(self,url):
        prompt = f"""
            Assuma que você é um assistente de um chatbot e que provavelmente o usuário esta enviando uma foto
            de uma pessoa ou tema referente a moda, beleza, cuidado com a pele ou produtos de beleza, maquiagem, higiene pessoal etc.
            Faça uma analise dele, e resua uma review a respeito sendo positivo ou negativo, de dicas sobre caso seja uma produto
            dicas de uso, caso seja uma pessoa faça um resumo sobre o look e aparecencia com uma nota de 0 a 10
            Processou uma imagem com o Vision e a resposta será informada no formato de saída

            #Formato de Saída:
            Minhas analises para a imagem são o seguinte:
            Review: [resultado de 0 a 10]
            [comentários gerais e dicas]

            ##Pontos Relevantes
            coloque Pontos Relevantes sobre a imagem
            """

        imagem_base64 = self.encodar_imagem(url)

        resposta = self.cliente.chat.completions.create(
            model=self.modelo,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": f"data:image/jpeg;base64,{imagem_base64}"}
                    ]
                }
            ],
            max_tokens=300,
        )
        return resposta.choices[0].message.content
