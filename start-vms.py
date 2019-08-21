#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

#
# This script is based on the oVirt sdk example scripts from Red Hat, Inc:
# https://github.com/oVirt/ovirt-engine-sdk/tree/master/sdk/examples
#

from time import sleep

import ovirtsdk4 as sdk
import ovirtsdk4.types as types

# put all VMs that should not start in this list:
ignore_list = ["Windows2008"]

connection = sdk.Connection(
    url='https://example.org/ovirt-engine/api',
    username='admin@internal',
    password='123456',
    ca_file='ca.pem',
    debug=True,
)

vms_service = connection.system_service().vms_service()
vms = vms_service.list()

for vm in vms:
    if vm.name not in ignore_list:
        if vm.status == types.VmStatus.DOWN:
            service = vms_service.vm_service(vm.id)
            
            print("Starting VM: {}".format(vm.name))
            service.start()
            
            is_down = True

            while is_down:
                sleep(5)
                get = service.get()
                if get.status == types.VmStatus.UP:
                    is_down = False

connection.close()

print('All VMs are up!')
