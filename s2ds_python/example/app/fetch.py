"""Module to fetch and parse website data.

"""
import requests
import logging

logger = logging.getLogger('example')

def fetch(url):
    """Fetch url and parse data.

    Args:
        url (str): web url to fetch
    """

    scheme = "http://"
    if not url.startswith(scheme):
        url = "{0}{1}".format(scheme, url)

    logger.info("Fetching {0}".format(url))
    return requests.get(url).text
