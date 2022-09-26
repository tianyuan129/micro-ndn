
import docker
            
class DockerNode:
    _name: str
    _image: str
    _mac: str
    _container_manager = docker.from_env().containers

    def __init__(self, image: str, name: str):
        self._image = image
        self._name = name
        self._container_manager.run(image = self._image, detach = True, name = self._name)
        self._container = docker.from_env().containers.get(self._name)
        self._mac = self._container.attrs['NetworkSettings']['Networks']['bridge']['MacAddress']

    def stop(self):
        self._container.stop()

    def remove(self):
        self._container.remove()
        
    def deploy_tar(self, tar_bytes, deploy_cmd: str):
        self._container.put_archive('/root', tar_bytes)
        self._container.exec_run(deploy_cmd)
    
    def start_nfd(self):
        self._container.exec_run('nfd', detach = True)
        
    def create_face(self, remote_uri: str):
        cmd_str = 'nfdc face create remote {} local dev://eth0 persistency permanent'.format(remote_uri)
        self._container.exec_run(cmd_str)
        
    def add_route(self, prefix: str, remote_uri: str):
        cmd_str = 'nfdc route add prefix {0} nexthop {1}'.format(prefix, remote_uri)
        self._container.exec_run(cmd_str)

    def set_multicast(self, prefix: str):
        cmd_str = 'nfdc strategy set prefix {0} strategy /localhost/nfd/strategy/multicast/v=4' \
                  .format(prefix)
        self._container.exec_run(cmd_str)
        
    def erase_cs(self, prefix: str):
        cmd_str = 'nfdc cs erase {0}'.format(prefix)
        self._container.exec_run(cmd_str)
