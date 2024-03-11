#!/usr/bin/env python

import json
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible import context
from ansible.module_utils.common.collections import ImmutableDict

# Load inventory
loader = DataLoader()
inventory = InventoryManager(loader=loader, sources='hosts.yml')
variable_manager = VariableManager(loader=loader, inventory=inventory)

context.CLIARGS = ImmutableDict(tags={}, listtags=False, listtasks=False, listhosts=False, syntax=False, connection='ssh',
                    module_path=None, forks=100, remote_user='xxx', private_key_file=None,
                    ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None, scp_extra_args=None, become=True,
                    become_method='sudo', become_user='root', verbosity=True, check=False, start_at_task=None)

# Run playbook
playbook_path = 'hello.yml'
playbook_executor = PlaybookExecutor(
    playbooks=[playbook_path],
    inventory=inventory,
    variable_manager=variable_manager,
    loader=loader,
    passwords={},
)
result = playbook_executor.run()

# Print playbook results
print("Playbook Results:")
print(json.dumps(result, indent=4))
