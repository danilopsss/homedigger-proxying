from hdproxying.round_robin import ProxyRotation, AVAILABLE_PROXIES


def test_proxy_rotation():
    proxy_rotation = ProxyRotation()
    iter_proxy = iter(proxy_rotation)
    assert next(iter_proxy) == AVAILABLE_PROXIES[0]
    assert next(iter_proxy) == AVAILABLE_PROXIES[1]
    assert next(iter_proxy) == AVAILABLE_PROXIES[0]
    assert next(iter_proxy) == AVAILABLE_PROXIES[1]
