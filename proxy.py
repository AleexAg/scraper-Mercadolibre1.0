import requests

proxies = {
    'http': 'x.x.x.x:80',
    'https': 'x.x.x.x:80',
}

proxies_one = {
    'http': 'x.x.x.x:80',
    'https': 'x.x.x.x:80',
}

proxies_two = {
    'http': 'x.x.x.x:80',
    'https': 'x.x.x.x:80',
}

proxies_three = {
    'http': 'x.x.x.x:80',
    'https': 'x.x.x.x:80',
}

def fetch(url:str):
    try:
        response = requests.get(url)
        #print("Fetch.. fetch_proxies", url)
        return response
    except Exception as error:
        print("Error fetch", error)


def fetch_proxies(url:str):
    try:
        response = requests.get(url, proxies=proxies)
        #print("Fetch.. fetch_proxies", url)
        return response
    except Exception as error:
        print("Error fetch", error)

def fetch_proxies_one(url:str):
    try:
        response = requests.get(url, proxies=proxies_one, timeout=5)
        #print("Fetch.. fetch_proxies_one", url)
        return response
    except Exception as error:
        pass
        #print("Error fetch", error)

def fetch_proxies_two(url:str):
    try:
        response = requests.get(url, proxies=proxies_two, timeout=5)
        #print("Fetch.. fetch_proxies_two", url)
        return response
    except Exception as error:
        pass
        #print("Error fetch", error)

def fetch_proxies_three(url:str):
    try:
        response = requests.get(url, proxies=proxies_three, timeout=5)
        #print("Fetch.. fetch_proxies_three", url)
        return response
    
    except Exception as error:
        pass
        #print("Error fetch", error)
