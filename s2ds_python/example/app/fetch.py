"""Module to fetch and parse website data.

"""
import requests

def fetch(url):
    """Fetch url and parse data.

    Args:
        url (str): web url to fetch
    """

    return requests.get(url).text()
