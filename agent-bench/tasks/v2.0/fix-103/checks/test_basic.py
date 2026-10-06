import csv
import io

from exporter import to_csv


def test_basic_unchanged():
    out = to_csv([{"name": "a", "note": 3}], ["name", "note"])
    assert list(csv.reader(io.StringIO(out))) == [["name", "note"], ["a", "3"]]
    assert out.endswith("\n")
