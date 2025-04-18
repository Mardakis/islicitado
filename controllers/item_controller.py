from models.item import Item

def buscar_todos_itens():
    itens = Item.get_all()
    return [
        {
            "id": item.id,
            "nome": item.nome,
            "quantidade": item.quantidade
        }
        for item in itens
    ]

def buscar_item_por_id(item_id):
    return Item.get_by_id(item_id)

def criar_item(nome, quantidade, processo_id):
    novo_item = Item(nome=nome, quantidade=quantidade, processo_id=processo_id)
    novo_item.save()
    return novo_item

def atualizar_item(item_id, nome=None, quantidade=None):
    item = Item.get_by_id(item_id)
    if not item:
        return False

    if nome:
        item.nome = nome
    if quantidade is not None:
        item.quantidade = quantidade

    item.save()
    return True

def deletar_item(item_id):
    item = Item.get_by_id(item_id)
    if not item:
        return False
    item.delete()
    return True
