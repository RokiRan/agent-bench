from loader import load_config


def test_port_override():
    assert load_config({"APP_PORT": "9090"})["port"] == "9090"


def test_host_override():
    assert load_config({"APP_HOST": "0.0.0.0"})["host"] == "0.0.0.0"
