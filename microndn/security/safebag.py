from ndn.encoding import parse_and_check_tl, TlvModel, ModelField, TypeNumber, NonStrictName, VarBinaryStr
from Cryptodome.PublicKey import ECC
from ndn.security import KeychainSqlite3, Identity, TpmFile
from ndn.app_support.security_v2 import parse_certificate, derive_cert, SafeBag, SecurityV2TypeNumber
from datetime import datetime
from typing import List
import tempfile

class SafeBagTlv(TlvModel):
    value = ModelField(SecurityV2TypeNumber.SAFE_BAG, SafeBag)

# safebag helper
def ecdsa_safebag_gen(keychain: KeychainSqlite3, cert_buf: VarBinaryStr, passwd: bytes) -> SafeBagTlv:
    this_cert = parse_certificate(cert_buf)
    signer = keychain.get_signer({'cert': this_cert.name})
    ecc_key = ECC.import_key(signer.key_der)
    encrypted_prv = ecc_key.export_key(format = 'DER', passphrase = passwd, use_pkcs8 = True, 
                                       protection = 'PBKDF2WithHMAC-SHA1AndAES128-CBC')
    safebag = SafeBag()
    safebag.certificate_v2 = parse_and_check_tl(cert_buf, TypeNumber.DATA)
    safebag.encrypted_key_bag = encrypted_prv
    
    safebag_wrapper = SafeBagTlv()
    safebag_wrapper.value = safebag
    return safebag_wrapper

def safebag_gen(signer_id: Identity, signer_keychain: KeychainSqlite3, newid_name: NonStrictName, keychain: KeychainSqlite3) -> SafeBagTlv:
    new_id = keychain.touch_identity(newid_name)
    new_key = new_id.default_key()
    new_cert = new_key.default_cert()
    new_cert_data = parse_certificate(new_cert.data)
    signed_cert_name, cert_buf = \
        derive_cert(new_key.name, 'microndn-signer', new_cert_data.content,
                    signer_keychain.get_signer({'identity': signer_id}),
                    datetime.now(), 3600 * 24 * 365)
    keychain.import_cert(new_key.name, signed_cert_name, cert_buf)
    return ecdsa_safebag_gen(keychain, cert_buf, '1234'.encode())

def safebag_gen2(anchor_id: Identity, keychain: KeychainSqlite3, names: List[NonStrictName]) -> List[SafeBagTlv]:
    with tempfile.TemporaryDirectory() as tmpdirname:
        tmp_pib_path = tmpdirname + '/pib.db'
        tmp_tpm_path = tmpdirname + '/tpm'
        KeychainSqlite3.initialize(tmp_pib_path, 'tpm-file', tmp_tpm_path)
        tmp_keychain = KeychainSqlite3(tmp_pib_path, TpmFile(tmp_tpm_path))
        return [safebag_gen(anchor_id, keychain, name, tmp_keychain) for name in names]