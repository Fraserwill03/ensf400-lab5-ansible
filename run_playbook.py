#!/usr/bin/env python

import ansible_runner
import os 
import requests

inventory_path = '/workspaces/ensf400-lab5-ansible/hosts.yml'
playbook_path = '/workspaces/ensf400-lab5-ansible/hello.yml'
config_path = '/workspaces/ensf400-lab5-ansible/ansible.cfg'

os.environ['ANSIBLE_CONFIG'] = config_path

results = ansible_runner.run(inventory=inventory_path, playbook=playbook_path)
print("\n\nPlaybook results:")
print(results.stats)

expected = [
    "Hello World from managedhost-app-1 !",
    "Hello World from managedhost-app-2 !",
    "Hello World from managedhost-app-3 !",
]

for i in range(0, 3):
    res = requests.get('http://localhost:80')
    if res.text == expected[i]:
        print("SUCCESSFUL RESPONSE")
    else:
        print("INCORRECT RESPONSE")
    print("Response from loadbalancer endpoint: ", res.text)