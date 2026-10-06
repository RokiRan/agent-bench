"""数据导出。"""


def to_csv(rows, headers):
    """把记录列表导出为 CSV 文本。rows 为 dict 列表。"""
    lines = [",".join(headers)]
    for row in rows:
        lines.append(",".join(str(row.get(h, "")) for h in headers))
    return "\n".join(lines) + "\n"
