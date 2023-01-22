import requests


def get_bytes_from_url(url: str) -> bytes:
    req = requests.get(url)
    return req.content
