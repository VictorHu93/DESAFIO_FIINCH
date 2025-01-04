from io import BytesIO
from PyPDF2 import PdfReader
import re

def extract_pdf_data(pdf_blob):
    """
    Extrai informações estruturadas de um PDF a partir de um blob.

    Args:
        pdf_blob (bytes): Dados binários do PDF.

    Returns:
        dict: Dados extraídos contendo número do processo, status, autor, documento do autor, réus e documentos dos réus.
    """
    try:
        reader = PdfReader(BytesIO(pdf_blob))
        text = ""
        for page in reader.pages:
            text += page.extract_text()

        # Extração do número do processo (ajustar o padrão conforme o texto do PDF)
        processo_numero_match = re.search(r"Processo\s*(Nº|No|Número):\s*([\d\/\-\.]+)", text, re.IGNORECASE)
        processo_numero = processo_numero_match.group(2).strip() if processo_numero_match else None

        # Extração do status
        status_match = re.search(r"Status:\s*([^\n]+)", text)
        status = status_match.group(1).strip() if status_match else None

        # Extração do autor
        autor_nome_match = re.search(r"Autor:\s*([^\n]+)", text)
        autor_nome = autor_nome_match.group(1).split("Documento Autor:")[0].strip() if autor_nome_match else None

        autor_doc_match = re.search(r"Documento Autor:\s*([\d\.\-]+)", text)
        autor_doc = autor_doc_match.group(1).strip() if autor_doc_match else None

        # Extração dos réus
        reus_matches = re.findall(r"Réu:\s*([^:\n]+)\s*Documento Réu:\s*([\d\.\-]+)", text)
        reus = [{"nome": match[0].strip(), "documento": match[1].strip()} for match in reus_matches]

        return {
            "processo_numero": processo_numero,
            "status": status,
            "autor_nome": autor_nome,
            "autor_documento": autor_doc,
            "reus": reus,
        }

    except Exception as e:
        raise ValueError(f"Erro ao processar PDF: {e}")

