from helpers import Helpers

class ToolsLumy(Helpers):
    def __init__(self):
        super().__init__()

    @property
    def tools(self):
        minha_tool = [
    {"type": "retrieval"},
    {
      "type": "function",
            "function": {
            "name": "validar_codigo_promocional",
            "description": "Valide um código promocional com base no arquivo promocional.txt",
            "parameters": {
                "type": "object",
                "properties": {
                    "codigo": {
                        "type": "string",
                        "description": "O código promocional, no formato, XXXXX. Por exemplo: BELEZA10",
                    },
                    "validade": {
                        "type": "string",
                        "description": f"A validade do cupom, caso seja válido. No formato DD/MM/YYYY.",
                    },
                },
                "required": ["codigo", "validade"],
            }
            }
            }
    
    ]
        return minha_tool

    def validar_codigo_promocional(self,args):
        codigo = args.get("codigo")
        validade = args.get("validade")
        
        return f"""
            #Formato Resposta
            {codigo} com validade: {validade}
            Ainda diga se é valido ou não para o usuário.
        """

    @property
    def lista_funcoes(self):
        minhas_funções={
            "validar_codigo_promocional":self.validar_codigo_promocional,
        }
        return minhas_funções