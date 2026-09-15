import json
import sys
from difflib import get_close_matches
from openai import OpenAI
BASE_URL = "http://localhost:1234/v1"
API_KEY = "lm-studio"
MODEL = "llama-3.2-3b-instruct"
PERGUNTA = "O livro Inteligência Artificial está disponível e quantos exemplares há?"
MAX_PASSOS = 6
SYSTEM = "Você é um assistente de biblioteca. Consulte as tools e, após receber o resultado, responda diretamente com título, disponibilidade e número de exemplares. Nunca invente dados nem dê uma despedida genérica."
_ACERVO = {
    "Engenharia de Software": {"disponivel": True, "exemplares": 4},
    "Inteligência Artificial": {"disponivel": True, "exemplares": 1},
    "Sistemas de Computação": {"disponivel": False, "exemplares": 0},
}
def listar_livros() -> list[str]:
    """Lista os títulos existentes no acervo da biblioteca."""
    return list(_ACERVO)

def consultar_livro(titulo: str) -> dict:
    """Consulta a disponibilidade e a quantidade de exemplares de um livro."""
    correspondencias = get_close_matches(titulo, _ACERVO, n=1, cutoff=0.7)
    if not correspondencias:
        raise ValueError(f"Livro desconhecido: {titulo}. Use listar_livros().")
    titulo_correto = correspondencias[0]
    return {"titulo": titulo_correto, **_ACERVO[titulo_correto]}

FUNCS = {"listar_livros": listar_livros, "consultar_livro": consultar_livro}
DESCRICOES = {
    "boa": (
        "Consulta se um livro está disponível e informa quantos exemplares existem. "
        "Use quando a pergunta mencionar um título específico."
    ),
    "ruim": "Executa uma operação interna.",
}

def criar_tools(modo: str) -> list[dict]:
    return [
        {
            "type": "function",
            "function": {
                "name": "listar_livros",
                "description": "Lista os títulos existentes no acervo da biblioteca.",
                "parameters": {"type": "object", "properties": {}},
            },
        },
        {
            "type": "function",
            "function": {
                "name": "consultar_livro",
                "description": DESCRICOES[modo],
                "parameters": {
                    "type": "object",
                    "properties": {"titulo": {"type": "string", "enum": list(_ACERVO)}},
                    "required": ["titulo"],
                },
            },
        },
    ]

def main() -> None:
    modo = sys.argv[1] if len(sys.argv) == 2 else ""
    if modo not in DESCRICOES:
        raise SystemExit("Uso: python agente.py boa|ruim")
    client = OpenAI(base_url=BASE_URL, api_key=API_KEY)
    tools = criar_tools(modo)
    mensagens = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": PERGUNTA},
    ]
    print(f"Modo: {modo} | Pergunta: {PERGUNTA}")
    for passo in range(1, MAX_PASSOS + 1):
        print(f"Passo {passo}/{MAX_PASSOS}")
        opcoes = {"model": MODEL, "messages": mensagens, "temperature": 0}
        if mensagens[-1]["role"] != "tool":
            opcoes["tools"] = tools
        resposta = client.chat.completions.create(**opcoes)
        mensagem = resposta.choices[0].message
        mensagens.append(mensagem.model_dump(exclude_none=True))
        if not mensagem.tool_calls:
            print(f"Resposta final: {mensagem.content}")
            return
        for chamada in mensagem.tool_calls:
            nome = chamada.function.name
            args = json.loads(chamada.function.arguments)
            print(f"Tool escolhida: {nome} | Argumentos: {args}")
            try:
                resultado = FUNCS[nome](**args)
            except (KeyError, TypeError, ValueError) as erro:
                resultado = {"erro": str(erro)}
            print(f"Resultado da tool: {resultado}")
            mensagens.append({
                "role": "tool", "tool_call_id": chamada.id,
                "content": "Dados confirmados; use-os na resposta final: " + json.dumps(resultado, ensure_ascii=False),
            })
    print(f"O agente atingiu o limite de {MAX_PASSOS} passos sem concluir.")

if __name__ == "__main__":
    main()