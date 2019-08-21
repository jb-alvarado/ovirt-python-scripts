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

connection = sdk.Connection(
    url='https://example.org/ovirt-engine/api',
    username='admin@internal',
    password='123456',
    ca_file='/etc/pki/ovirt-engine/ca.pem',
    debug=True,
)

vms_service = connection.system_service().vms_service()
vms = vms_service.list()

shutdown_list = []

for vm in vms:
    if vm.status == types.VmStatus.UP:
        shutdown_list.append(vm.id)
        service = vms_service.vm_service(vm.id)

        print("Stopping VM: {}".format(vm.name))
        service.shutdown()

        sleep(0.5)

while True:
    for id in shutdown_list:
        service = vms_service.vm_service(id)
        get = service.get()

        if get.status == types.VmStatus.DOWN:
            shutdown_list.remove(id)
            break
    else:
        break

    sleep(1)

connection.close()

sleep(1)
print('All VMs are down!')
