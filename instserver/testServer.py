import requests
import json
import pickle
from time import sleep

if __name__ == "__main__":
    d = json.dumps({'name': 'd', 'method': 'idn', 'arguments': None})
    r = requests.post(" http://127.0.0.1:5000/Trigger", data=d)
    d = json.dumps({'name': 'd', 'method': 'measure', 'arguments': 2000})
    r = requests.post(" http://127.0.0.1:5000/Trigger", data=d)

    sleep(2)

    d = json.dumps({'name': 'd', 'method': 'idn'})
    r = requests.post("http://127.0.0.1:5000/Read", data=d)
    print(r.status_code, r.reason)
    print(pickle.loads(r.content))

    d = json.dumps({'name': 'd', 'method': 'measure'})
    r = requests.post("http://127.0.0.1:5000/Read", data=d)
    print(r.status_code, r.reason)
    print(pickle.loads(r.content))

    print('===========GET==========')
    r = requests.get("http://127.0.0.1:5000/Read",params={'name': 'd', 'method': 'measure'})
    print(pickle.loads(r.content))