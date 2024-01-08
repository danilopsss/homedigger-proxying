import os
import urllib3
import requests
from collections import namedtuple


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Proxies:

    Error = namedtuple("Error", ["status_code", "content"])

    @classmethod
    def scraperapi(cls, url: str):
        api_key = os.getenv("PROVIDER_SCRAPPER_API")
        proxy = f"scraperapi.country_code=eu.render=true:{api_key}@proxy-server.scraperapi.com:8001"
        proxies = {
            "https": proxy,
            "http": proxy,
        }
        try:
            response = requests.get(url, proxies=proxies, verify=False)
        except requests.exceptions.ConnectionError:
            response = cls.Error(status_code=500, content="")
        return response

    @classmethod
    def zenrows(cls, url: str):
        api_key = os.getenv("PROVIDER_ZEN_ROWS")
        proxy = f"http://{api_key}:js_render=true&premium_proxy=true&proxy_country=es@proxy.zenrows.com:8001"
        proxies = {
            "http": proxy,
            "https": proxy
        }
        try:
            response = requests.get(url, proxies=proxies, verify=False)
        except requests.exceptions.ConnectionError:
            response = cls.Error(status_code=500, content="")
        return response


AVAILABLE_PROXIES = (
    Proxies.scraperapi,
    Proxies.zenrows 
)
