from models.log import Log

def registrar_log(usuario_id, acao, descricao):
    log = Log(usuario_id=usuario_id, acao=acao, descricao=descricao)
    log.save()

def listar_logs():
    return Log.get_all()
