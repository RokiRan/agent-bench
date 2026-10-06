from fetcher import fetch


def ping(url):
    code, _ = fetch(url, 0)
    return code == 200
