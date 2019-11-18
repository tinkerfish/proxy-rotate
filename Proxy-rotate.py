import requests
import time
from random import choice
import multiprocessing
import concurrent.futures
import threading


class ProxyRotate:
    def __init__(self):
        self.url = 'https://www.proxy-list.download/api/v1/get?type=https&anon=elite'
        self.response = requests.get(self.url)
        self.raw_proxies = self.response.text.split("\r\n")
        self.working_proxies = []

    def check_proxy(self, proxy):
        url = "https://httpbin.org/ip"
        print("Checking Proxy: {}".format(proxy))
        try:
            response = requests.get(url, proxies={"http": proxy, "https": proxy}, timeout=5)
            print(response.json())
            self.working_proxies.append(proxy)
        except requests.exceptions.ConnectTimeout:
            print(proxy, ": Connection Failure")
        except Exception as e:
            print("Error: ", e)

    def clean_proxies(self):
        executor = concurrent.futures.ThreadPoolExecutor(10)
        futures = [executor.submit(self.check_proxy, proxy) for proxy in self.raw_proxies]
        concurrent.futures.wait(futures)

    def rotate_proxy(self):
        random_proxy = choice(self.working_proxies)
        return {
            "http": random_proxy,
            "https": random_proxy,
        }


if __name__ == "__main__":
    p = ProxyRotate()
    p.clean_proxies()
    print(p.working_proxies)
