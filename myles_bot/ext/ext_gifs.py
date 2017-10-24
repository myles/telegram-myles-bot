import requests


def all_gifs():
    resp = requests.get('https://gifs.mylesb.ca/api.json')

    return resp.json()
