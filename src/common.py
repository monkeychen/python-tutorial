import matplotlib.pyplot as plt

import requests
import json
import re

print("hello py3!")

str1 = ('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
        '-bbbbaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
print(str1)

resp = requests.request('GET', 'http://www.baidu.com', data=json.dumps({}), headers={})
print(resp.content)

l = [{'k': 11, 'n': 'n1'}, {'k': 22, 'n': 'n2'}]
print(max(l, key=lambda item: item['k']))

arr = re.findall('.{2}', '12345678')
print(arr)



