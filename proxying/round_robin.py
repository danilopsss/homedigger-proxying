import time
from .available_proxies import AVAILABLE_PROXIES


class ProxyRotation:

    def __init__(self, retries: int = 5):
        self._current_pos = -1
        self._wait_for_retry = retries
        self._retries = {
            proxy: {"retries": 0, "logs": []}
            for proxy in AVAILABLE_PROXIES
        }
    
    @property
    def wait_for_retry(self):
        return self._wait_for_retry

    @property
    def index(self):
        return self._current_pos
    
    @property
    def proxies(self):
        filter_ = filter(
            lambda key: self._retries[key]["retries"] < 3,
            self._retries.keys()
        )
        return list(filter_)
    
    def register_proxy_availability(self, proxy, log, reset: bool = False):
        if not reset:
            self._retries[proxy]["retries"] += 1
            self._retries[proxy]["logs"].append(log)
            time.sleep(self.wait_for_retry)
        self._retries[proxy]["retries"] = 0

    def __iter__(self):
        return self
    
    def __next__(self):
        self._current_pos += 1
        if self.index > len(self.proxies) - 1:
            self._current_pos = 0
        proxy = AVAILABLE_PROXIES[self.index]
        if self._retries[proxy]["retries"] > 3:
            raise StopIteration("No proxies available")
        return proxy
