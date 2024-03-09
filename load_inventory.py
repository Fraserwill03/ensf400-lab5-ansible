#!/usr/bin/env python

import json
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase

# Custom callback to capture ping results
class ResultsCollector(CallbackBase):
    def __init__(self):
        super(ResultsCollector, self).__init__()
        self.successful = {}
        self.unreachable = {}
        self.failed = {}
    
    def v2_runner_on_unreachable(self, result):
        host = result._host
        self.host_unreachable[host.get_name()] = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        host = result._host
        self.host_failed[host.get_name()] = result

    def v2_runner_on_ok(self, result, **kwargs):
        host = result._host.get_name()
        self.successful[host] = result

# Load inventory
loader = DataLoader()
inventory = InventoryManager(loader=loader, sources='hosts.yml')
variable_manager = VariableManager(loader=loader, inventory=inventory)

# Print host information
print("Hosts:")
for host in inventory.get_hosts():
    host_vars = variable_manager.get_vars(host=host)
    print(f"Name: {host}, IP: {host_vars['ansible_host']}, Groups: {host_vars['group_names']}")

# Ping hosts
print("\nPing results:")
play_source = dict(
    name="Ping hosts",
    hosts="all",
    gather_facts="no",
    tasks=[dict(action=dict(module='ping'), register='ping_result')]
)
play = Play().load(play_source, variable_manager=variable_manager, loader=loader)
tqm = TaskQueueManager(
    inventory=inventory,
    variable_manager=variable_manager,
    loader=loader,
    passwords=dict(),
    stdout_callback=ResultsCollector(),
)
result = tqm.run(play)
ping_results = {
    "SUCCESS": tqm._stdout_callback.successful, 
    "FAILED": tqm._stdout_callback.failed, 
    "UNREACHABLE": tqm._stdout_callback.unreachable
}

# Iterates throguh successful AND unsuccessful results
for key in ping_results.keys():
    for host, result in ping_results.get(key).items():
        print(f"{host} | {key} => {json.dumps(result._result, indent=4)[1:-1]}")
