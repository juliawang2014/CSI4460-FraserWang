from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import configparser

"""
parameters = dh.generate_parameters(generator=2, key_size=512)

private_key = parameters.generate_private_key()
peer_public_key = parameters.generate_private_key().public_key()
shared_key = private_key.exchange(peer_public_key)
derived_key = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=b'handshake data',
).derive(shared_key)

private_key_2 = parameters.generate_private_key()
peer_public_key_2 = parameters.generate_private_key().public_key()
shared_key_2 = private_key_2.exchange(peer_public_key_2)
derived_key_2 = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=b'handshake data',
).derive(shared_key_2)
print("Base parameters")
print(parameters.parameter_numbers().p)
print(parameters.parameter_numbers().g)
print("Peer public key 1 derived parameters")
print(peer_public_key.public_numbers().parameter_numbers.p)
print(peer_public_key.public_numbers().parameter_numbers.g)
print("Peer public key 2 derived parameters")
print(peer_public_key_2.public_numbers().parameter_numbers.p)
print(peer_public_key_2.public_numbers().parameter_numbers.g)
"""
def storeParameters():
    parameters = dh.generate_parameters(generator=2, key_size=512)
    pn = parameters.parameter_numbers()
    p = pn.p
    g = pn.g
    y = 10
    config = configparser.ConfigParser()
    config['PARAMETERS'] = {'p': p, 'g': g, 'y': y}
    with open ('parameters.config', 'w') as configfile:
        config.write(configfile)

def getSharedKey(params):
    private_key = params.generate_private_key()
    peer_public_key = params.generate_private_key().public_key()
    shared_key = private_key.exchange(peer_public_key)
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data',
    ).derive(shared_key)
    return derived_key

