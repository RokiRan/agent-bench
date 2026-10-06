import csv
import io

from exporter import to_csv


def parse(text):
    return list(csv.reader(io.StringIO(text)))


def test_fields_with_commas():
    out = to_csv([{"name": "张三, 经理", "note": "OK"}], ["name", "note"])
    assert parse(out)[1] == ["张三, 经理", "OK"]


def test_fields_with_quotes_and_newlines():
    out = to_csv([{"name": '说"你好"', "note": "第一行\n第二行"}], ["name", "note"])
    assert parse(out)[1] == ['说"你好"', "第一行\n第二行"]
