import os
import shutil
from models.anexo import Anexo
from datetime import datetime

UPLOAD_DIR = "uploads"

def salvar_anexo_temp(arquivo_path, nome_original, processo_id):
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    extensao = os.path.splitext(nome_original)[1]
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    novo_nome = f"{timestamp}_{nome_original}"
    destino = os.path.join(UPLOAD_DIR, novo_nome)

    shutil.copy(arquivo_path, destino)

    anexo = Anexo(
        nome_arquivo=nome_original,
        caminho=destino,
        processo_id=processo_id
    )
    anexo.save()

    return True, "Arquivo anexado com sucesso."

def listar_anexos_do_processo(processo_id):
    return Anexo.get_by_processo(processo_id)
