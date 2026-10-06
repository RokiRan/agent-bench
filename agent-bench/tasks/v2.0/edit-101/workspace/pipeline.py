from fetcher import fetch


def run(url):
    code, content = fetch(url, 1)  # 位置传参：只要 1 次重试
    return f"{code} {content}"
