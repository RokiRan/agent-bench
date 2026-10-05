"""定价规则。"""


def apply_discount(amount, discount):
    """对金额应用折扣（discount=0.1 表示九折），保留两位小数。"""
    return round(amount * (1 - discount), 2)
