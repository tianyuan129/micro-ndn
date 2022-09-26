from typing import Callable
from os import getlogin
from .node import DockerNode
import docker

ContainerNaming = Callable[[int], str]

class DockerSession:
    _session: int
    _container_image_repo = 'tianyuan129/ndn-basic'
    _container_image_tag = 'latest'
    _container_names: dict[int : str]
    containers: dict[str : DockerNode]
    mac_addr: dict[str, str]
    _container_manager = docker.from_env().containers

    def __init__(self, session: int):
        self.containers = {}
        self.mac_addrs= {}
        self._session = session
    
    def _container_naming(self, index):
        return getlogin() + '-session' + str(self._session)\
                          + '-instance' + str(index)

    def _check_image_exist(self):
        _image_manager = docker.from_env().images
        _image_name = self._container_image_repo + ':' + self._container_image_tag
        try:
            _image_manager.get(_image_name)
        except docker.errors.ImageNotFound:
            _image_manager.pull(self._container_image_repo, self._container_image_tag)
            
    def set_names(self, num: int, naming: ContainerNaming = None):
        if naming is None:
            self._container_names = {i: self._container_naming(i) for i in range(1, num + 1)}
        else: 
            self._container_names = {i: naming(i) for i in range(1, num + 1)}       
    
    def start(self, num: int, naming: ContainerNaming = None):
        self.set_names(num, naming)
        self._check_image_exist()
        _image_name = self._container_image_repo + ':' + self._container_image_tag
        for _cn in self._container_names:
            this_container = DockerNode(_image_name, self._container_names[_cn])
            self.containers[self._container_names[_cn]] = this_container
            self.mac_addrs[self._container_names[_cn]] = this_container._mac

    def kill(self):
        for _cn in self.containers:
            self.containers[_cn].stop()
            self.containers[_cn].remove()

    def create_face(self, local: DockerNode, remote: DockerNode):
        uri_str = 'ether://[{}]'.format(remote._mac)
        local.create_face(uri_str)
        
    def create_interface(self, lhs: DockerNode, rhs: DockerNode):
        self.create_face(lhs, rhs)
        self.create_face(rhs, lhs)

    def add_route(self, prefix: str, local: DockerNode, remote: DockerNode):
        uri_str = 'ether://[{}]'.format(remote._mac)
        local.add_route(prefix, uri_str)
    
        