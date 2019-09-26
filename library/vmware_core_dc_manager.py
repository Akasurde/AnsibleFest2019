#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Abhijeet Kasurde <akasurde@redhat.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: vmware_core_dc_manager
short_description: Create Datacenter using REST APIs
description:
- Create datacenter using REST API.
- This module is based on REST API and uses httpapi connection plugin for persistent connection.
version_added: '2.9'
author:
- Abhijeet Kasurde (@Akasurde)
notes:
- Tested on vSphere 6.7
requirements:
- python >= 2.6
options:
  datacenter_name:
    description:
    - Name of the datacenter
    type: str
extends_documentation_fragment: VmwareRestModule_filters.documentation
'''

EXAMPLES = r'''

- name: Create datacenter
  vmware_core_dc_manager:
    datacenter_name: 'Asia-Datacenter5'
  register: dc_results
'''

RETURN = r'''#
'''

from ansible.module_utils.vmware_httpapi.VmwareRestModule import VmwareRestModule


def main():
    argument_spec = VmwareRestModule.create_argument_spec(use_filters=True)
    argument_spec.update(
        datacenter_name=dict(type='str'),
        folder_name=dict(type='str')
    )

    module = VmwareRestModule(argument_spec=argument_spec,
                              supports_check_mode=True,
                              use_object_handler=True)
    
    url = '/rest/vcenter/datacenter'
    folder_name = module.params.get('folder_name')
    dc_name = module.params.get('datacenter_name')

    data_body = {
        'spec': {
            'folder': folder_name,
            'name': dc_name,
        }
    }
    import json
    module.post(url=url, data=data_body) #json.dumps(data_body))
    module.exit()


if __name__ == '__main__':
    main()
