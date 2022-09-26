import tempfile
from time import sleep
from ndn.security import TpmFile, KeychainSqlite3
from ndn.app_support.security_v2 import parse_certificate
import os
from random import randint

from microndn.security.bootstrap import Bootstraper
from microndn.docker_support.session import DockerSession

instance_num = 3
session = DockerSession(randint(1, 1000))
session.start(instance_num)
print(session.mac_addrs)

anchor_keychain = KeychainSqlite3(os.path.expanduser('~/.ndn/pib.db'),
                                  TpmFile(os.path.expanduser('~/.ndn/ndnsec-key-file')))
try:
    anchor_id = anchor_keychain['/ndn/site1']
except:
    anchor_id = anchor_keychain.touch_identity('/ndn/site1')
anchor_key = anchor_id.default_key()
anchor_cert = anchor_key.default_cert()
anchor_cert_data = parse_certificate(anchor_cert.data)

boot = Bootstraper(anchor_id, anchor_keychain)
with tempfile.TemporaryDirectory() as tmpdirname:
    for index in range(1, instance_num + 1):
        boot.export_files(tmpdirname, '/ndn/site1/instance' + str(index))
        tar_file = tmpdirname + '/bootstrap.tar'
        boot.export_tar(tmpdirname, tar_file)
        this_node_name = session._container_names[index]
        this_node = session.containers[this_node_name]
        with open(tar_file, 'rb') as tar_file_bytes:
            this_node.deploy_tar(tar_file_bytes.read(), boot.get_bootstrap_cmd())
        # starting nfd first
        this_node.start_nfd()

# setting up connectivity
sleep(2)
node1 = session.containers[session._container_names[1]]
node2 = session.containers[session._container_names[2]]
node3 = session.containers[session._container_names[3]]
session.create_interface(node1, node2)
session.create_interface(node1, node3)
session.create_interface(node2, node3)
session.add_route('/ndn/site1', node1, node2)
node1.set_multicast('/ndn/site1')
node1.erase_cs('/ndn/site1')

# comment this if you want to keep the containers
session.kill()