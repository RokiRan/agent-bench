from csvtool import csv_total


def test_total_on_fixture():
    assert csv_total("data.csv") == 15.0
