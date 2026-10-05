from csvtool import csv_total


def test_skips_bad_rows(tmp_path):
    p = tmp_path / "t.csv"
    p.write_text("id,amount\n1,2.5\n2,oops\n3,1.5\n", encoding="utf-8")
    assert csv_total(str(p)) == 4.0


def test_header_only(tmp_path):
    p = tmp_path / "t.csv"
    p.write_text("id,amount\n", encoding="utf-8")
    assert csv_total(str(p)) == 0.0
