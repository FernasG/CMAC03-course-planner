import fitz  # PyMuPDF
import re
import json

def extrair_dados_do_pdf(caminho_pdf):
    with fitz.open(caminho_pdf) as doc:
        texto = "\n".join([page.get_text() for page in doc])

    # Normaliza o texto (remove múltiplos espaços e quebras de linha extras)
    texto = re.sub(r'\s{2,}', ' ', texto)
    texto = re.sub(r'\n+', '\n', texto)

    # Curso (fixo)
    if "CIÊNCIA DA COMPUTAÇÃO/IMC" in texto:
        curso = "cco"
    elif "SISTEMAS DE INFORMAÇÃO/IMC" in texto:
        curso = "sin"
    else:
        curso = "desconhecido"

    # Período letivo atual
    periodo = ""
    match_periodo = re.search(r"Perfil Inicial:\s*\d+\s*\n(\d+)", texto)
    if match_periodo:
        periodo = match_periodo.group(1)
   

    # Carga horária optativas pendentes
    ch_optativas_pendentes = "0"
    trecho_optativas = re.search(r"Optativas.*?(\d+\s*h.*?){3}", texto)
    if trecho_optativas:
        horas = re.findall(r"(\d+)\s*h", trecho_optativas.group(0))
        if len(horas) >= 3:
            ch_optativas_pendentes = horas[2]  # 3ª ocorrência = PENDENTE

    # Disciplinas pendentes (a seção começa com "Componentes Curriculares Obrigatórios Pendentes")
    pendentes_raw = re.search(r"Componentes Curriculares Obrigatórios Pendentes:(.*?)Optativas", texto, re.DOTALL)
    disciplinas_pendentes = []

    if pendentes_raw:
        # Procura por códigos como CRSC03, MAT00A, TCC1-140H etc.
        disciplinas_pendentes = re.findall(r"([A-Z]{2,4}[A-Z]?\d{2,3}[A-Z]?(?:-\d{3}H)?)", pendentes_raw.group(1))
        disciplinas_pendentes = list(dict.fromkeys(disciplinas_pendentes))  # remove duplicatas

    return {
        "curso": curso,
        "periodo": periodo,
        "ch_optativas_pendentes": ch_optativas_pendentes,
        "disciplinas_pendentes": disciplinas_pendentes
    }

# --------- EXECUÇÃO EXEMPLO ----------
caminho_pdf = "historico_SIN-2.pdf"
dados = extrair_dados_do_pdf(caminho_pdf)

# Salvar como JSON
with open("resultado.json", "w", encoding="utf-8") as f:
    json.dump(dados, f, indent=2, ensure_ascii=False)

# Mostrar no terminal
print(json.dumps(dados, indent=2, ensure_ascii=False))
