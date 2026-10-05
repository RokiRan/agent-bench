def remove_out_of_stock(inventory):
    """移除库存为 0 的商品，返回更新后的字典。"""
    for name, count in inventory.items():
        if count == 0:
            del inventory[name]
    return inventory
