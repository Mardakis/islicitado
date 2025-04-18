from models.consumo import Consumo
from models.item import Item

def registrar_consumo(item_id, usuario_id, quantidade):
    item = Item.get_by_id(item_id)

    if item is None:
        return False, "Item não encontrado."

    if item.quantidade < quantidade:
        return False, "Quantidade insuficiente em estoque."

    # Atualiza quantidade do item
    nova_quantidade = item.quantidade - quantidade
    item.quantidade = nova_quantidade
    item.save()

    # Registra consumo
    consumo = Consumo(item_id=item_id, usuario_id=usuario_id, quantidade=quantidade)
    consumo.save()

    return True, "Consumo registrado com sucesso."

def listar_consumos_por_item(item_id):
    return Consumo.get_by_item_id(item_id)

def listar_todos_os_consumos():
    return Consumo.get_all()
