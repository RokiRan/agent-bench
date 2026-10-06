from dedupe import dedupe_keep_last


def test_example():
    records = [{"id": 1, "v": "a"}, {"id": 2, "v": "b"}, {"id": 1, "v": "c"}]
    assert dedupe_keep_last(records, "id") == [{"id": 2, "v": "b"}, {"id": 1, "v": "c"}]


def test_missing_key_kept_in_place():
    records = [{"id": 1}, {"v": "x"}, {"id": 1, "v": "b"}, {"v": "y"}]
    assert dedupe_keep_last(records, "id") == [{"v": "x"}, {"id": 1, "v": "b"}, {"v": "y"}]
