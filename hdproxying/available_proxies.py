import os
import urllib3
import requests
from collections import namedtuple


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Proxies:
    Error = namedtuple("Error", ["status_code", "content"])

    @classmethod
    def bright_data(cls, url: str):
        api_key = os.getenv("PROVIDER_BRIGHTDATA_API")
        proxy = f"http://brd-customer-hl_e1b0c685-zone-unblocker:{api_key}@brd.superproxy.io:22225"

        proxies = {
            "https": proxy,
        }
        try:
            response = requests.get(url, proxies=proxies, verify=False)
        except requests.exceptions.ConnectionError:
            response = cls.Error(status_code=500, content="")
        return response

    @classmethod
    def scraperapi(cls, url: str):
        api_key = os.getenv("PROVIDER_SCRAPPER_API")
        call_url = f"http://api.scraperapi.com?api_key={api_key}"
        params = {"url": url}
        try:
            response = requests.get(call_url, params=params)
        except requests.exceptions.ConnectionError:
            response = cls.Error(status_code=500, content="")
        return response

    @classmethod
    def zenrows(cls, url: str):
        api_key = os.getenv("PROVIDER_ZEN_ROWS")
        proxy = f"http://{api_key}:premium_proxy=true&proxy_country=es@proxy.zenrows.com:8001"
        proxies = {"http": proxy, "https": proxy}
        try:
            response = requests.get(url, proxies=proxies, verify=False)
        except requests.exceptions.ConnectionError:
            response = cls.Error(status_code=500, content="")
        return response

    @classmethod
    def scrapeops(cls, url: str):
        api_key = os.getenv("PROVIDER_SCRAPEOPS")
        params = {
            'api_key': api_key,
            'url': url,
        }
        try:
            response = requests.get(url, params=params)
        except requests.exceptions.ConnectionError:
            response = cls.Error(status_code=500, content="")
        return response


AVAILABLE_PROXIES = (
    Proxies.scraperapi,
    Proxies.bright_data,
    Proxies.zenrows,
    Proxies.scrapeops
)
