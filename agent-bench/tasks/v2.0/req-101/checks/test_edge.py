from dedupe import dedupe_keep_last


def test_empty():
    assert dedupe_keep_last([], "id") == []


def test_none_key_returns_copy():
    records = [{"id": 1}, {"id": 1}]
    out = dedupe_keep_last(records, None)
    assert out == records
    assert out is not records


def test_input_not_mutated():
    records = [{"id": 1}, {"id": 1, "v": "b"}]
    dedupe_keep_last(records, "id")
    assert records == [{"id": 1}, {"id": 1, "v": "b"}]
