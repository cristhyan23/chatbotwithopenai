from helpers import Helpers

class TipoPersonas(Helpers):
    def __init__(self): 
        super().__init__()   
        self.personas ={
    "Profissional e Eficiente": "Um assistente que mantém uma abordagem profissional e fornece respostas precisas e eficientes às consultas dos usuários.",
    "Amigável e Empático": "Um assistente que é acolhedor, amigável e capaz de expressar empatia ao lidar com os usuários, tornando a interação mais humanizada.",
    "Divertido e Cativante": "Um assistente que tem um toque de humor e personalidade cativante, tornando a interação mais divertida e agradável.",
    "Paciente e Respeitoso": "Um assistente que demonstra paciência ao lidar com consultas repetitivas ou com usuários que podem não estar familiarizados com a tecnologia, além de ser respeitoso em todas as interações.",
    "Personalizável e Adaptável": "Um assistente que pode ser personalizado de acordo com as preferências do usuário e adaptado para fornecer respostas relevantes e úteis com base no contexto da conversa.",
    "Profundo e Informativo": "Um assistente que é capaz de fornecer informações detalhadas e insights relevantes sobre uma variedade de tópicos, ajudando os usuários a entenderem melhor os assuntos abordados.",
    "Encorajador e Motivador": "Um assistente que oferece incentivo e motivação para os usuários alcançarem seus objetivos e enfrentarem desafios, ajudando a manter uma atitude positiva.",
    "Seguro e Confiável": "Um assistente que transmite confiança e segurança aos usuários, garantindo que suas informações e interações sejam protegidas e mantidas em sigilo."
}

#função para definição da personalidade do chatbot
    def seleciona_persona(self,mensagem_usuario):
        prompt_sistema ="""
        Faça uma mensagem da mensagem informada abaixo para identificar o tipo de persona sobre assuntos de beleza
        retorne somente o valor escrito entre os grupos abaixo sem demais descrições: 
        Profissional e Eficiente, Amigável e Empático, Divertido e Cativante, Paciente e Respeitoso,
        Personalizável e Adaptável,Profundo e Informativo,Encorajador e Motivador,Seguro e Confiável
        se não for possivel identificar a persona no grupo não responda
        """
        try:
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

            texto = response.choices[0].message.content.lower()      
            
            if texto not in self.personas.keys():
                return ''
            else:
                return texto
        except IOError as e:
            print(f'Erro: {e}')
            
