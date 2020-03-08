import requests
from concurrent.futures import ThreadPoolExecutor

nr_batches = 10
batch = 50

def make_request():
    response = requests.get("http://127.0.0.1:5000")
    return response.status_code

with ThreadPoolExecutor(max_workers=batch) as executor:
    for i in range(nr_batches):
        for j in range(batch):
            future = executor.submit(make_request)
            print(future.result())
