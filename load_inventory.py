#!/usr/bin/env python

import ansible_runner
import sys
import os

inventory_path = './hosts.yml'
config_path = './ansible.cfg'

# Load inventory using ansible_runner
inventory = ansible_runner.get_inventory(action='list', inventories=[inventory_path], response_format='json', quiet=True)
info = inventory[0]['_meta']['hostvars']
groups = inventory[0]['all']['children']

# Print host information
print("Host Information:")
for group in groups:
    try:
        for host in inventory[0][group]['hosts']:
            print(f"Name: {host}, IP: {info[host]['ansible_host']}, Groups: {group}")
    except KeyError:
        continue

# Set env vars so the command will run correctly
# This is needed because the ansible config is in a world writeable directory
# So ansible does not automatically read from the config file
os.environ['ANSIBLE_CONFIG'] = config_path

print("\nPing results")
# Please note that the run_command prints the output on its own
ansible_runner.run_command(
    executable_cmd='ansible',
    cmdline_args=['all:localhost', '-m', 'ping'],
    input_fd=sys.stdin,
    output_fd=sys.stdout,
    error_fd=sys.stderr,
)


