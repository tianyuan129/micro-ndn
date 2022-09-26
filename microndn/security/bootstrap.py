from .safebag import *
from ..utils.b64_writer import write_base64_file
import tarfile

class Bootstraper:
    _anchor_file_name = 'trust-anchor.ndncert'
    _safebag_file_name = 'identity.ndnkey'
    
    def __init__(self, anchor_id: Identity, anchor_keychain: KeychainSqlite3):
        self.anchor_id = anchor_id
        self.anchor_keychain = anchor_keychain
        self.anchor_cert = anchor_id.default_key().default_cert().data
    
    def export_files(self, file_path: str, id_name: NonStrictName):
        write_base64_file(file_path + '/' + self._anchor_file_name, self.anchor_cert)
        safebag_tlv = safebag_gen2(self.anchor_id, self.anchor_keychain, [id_name])
        write_base64_file(file_path + '/' + self._safebag_file_name, safebag_tlv[0].encode())
        
    def export_tar(self, file_path: str, tar_path: str):
        tar = tarfile.TarFile(tar_path, mode='w')
        tar.add(name = file_path + '/' + self._anchor_file_name,
                arcname = self._anchor_file_name)
        tar.add(name = file_path + '/' + self._safebag_file_name,
                arcname = self._safebag_file_name)
        tar.close()
        
    def get_bootstrap_cmd(self) -> str:
        bash = ''
        bash += 'ndnsec import ' + self._safebag_file_name + ' -P 1234'
        return bash

