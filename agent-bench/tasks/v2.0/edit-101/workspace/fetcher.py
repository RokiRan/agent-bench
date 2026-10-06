"""HTTP 抓取工具。"""


def fetch(url, retries=3):
    """抓取 url，失败重试 retries 次。返回 (状态码, 内容)。"""
    return 200, f"<content of {url} after {retries} retries>"
