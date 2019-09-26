#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2018, Ansible Project
# Copyright: (c) 2018, Abhijeet Kasurde <akasurde@redhat.com>
#
#  GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: vmware_datacenter_manager
short_description: Manage VMware Datacenter
description:
- Manage datacenters
author:
- Abhijeet Kasurde (@Akasurde)
notes:
- Tested on vSphere 6.5
requirements:
- python >= 2.6
- PyVmomi
- vSphere Automation SDK
extends_documentation_fragment: vmware_rest_client.documentation
'''

EXAMPLES = r'''
- name: Create datacenter
  vmware_datacenter_manager:
    hostname: '{{ vcenter_hostname }}'
    username: '{{ vcenter_username }}'
    password: '{{ vcenter_password }}'
    datacenter: '{{ datacenter_name }}'
  delegate_to: localhost

'''

RETURN = r'''# 
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.vmware_rest_client import VmwareRestClient
from com.vmware.vcenter_client import (Datacenter, Folder)


class VmDCManager(VmwareRestClient):
    def __init__(self, module):
        """Constructor."""
        super(VmDCManager, self).__init__(module)
        self.module = module
        self.dc_service = self.api_client.vcenter
        self.datacenter_name = self.params.get('datacenter_name')

    def check_dc_state(self):
        names = set([self.datacenter_name])
        datacenter_summaries = self.dc_service.Datacenter.list(Datacenter.FilterSpec(names=names))
        if len(datacenter_summaries) > 0:
            return True
        return False

    def ensure_state(self):
        dc_status = self.check_dc_state()
        if not dc_status:
            folder_summaries = self.dc_service.Folder.list(Folder.FilterSpec(type=Folder.Type.DATACENTER))
            folder = folder_summaries[0].folder

            datacenter1 = self.dc_service.Datacenter.create(
                Datacenter.CreateSpec(name=self.datacenter_name, folder=folder))
            self.module.exit_json(changed=True, datacenter_status="%s is created" % datacenter1)
        self.module.exit_json(changed=False, datacenter_status="%s already exists" % self.datacenter_name)


def main():
    argument_spec = VmwareRestClient.vmware_client_argument_spec()
    argument_spec.update(
        datacenter_name=dict(type='str', required=True),
    )

    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=False)
    dc_status = VmDCManager(module)
    dc_status.ensure_state()


if __name__ == '__main__':
    main()
