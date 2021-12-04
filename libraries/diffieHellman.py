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
"""

config = configparser.ConfigParser()

def getSharedKeyFromFile():
    config.read('parameters.config')
    sharedKey = int(config['PARAMETERS']['sharedKey'])
    return sharedKey

def storeSharedKeyToFile(sharedKey):
    config.read('parameters.config')
    config['PARAMETERS']['sharedKey'] = sharedKey
    with open ('parameters.config', 'w') as configfile:
        config.write(configfile)
        
def getPrivateKeyFromFile():
    config.read('parameters.config')
    privateKey = int(config['PARAMETERS']['x'])
    return privateKey
        
def storePrivateKeyToFile(privateKey):
    config.read('parameters.config')
    config['PARAMETERS']['x'] = privateKey
    with open ('parameters.config', 'w') as configfile:
        config.write(configfile)
        
def generateNewPrivateKey():
    config.read('parameters.config')
    p = int(config['PARAMETERS']['p'])
    g = int(config['PARAMETERS']['g'])
    pn = dh.DHParameterNumbers(p, g)
    parameters = pn.parameters()
    private_key = parameters.generate_private_key()
    return private_key
    
def generateNewPublicKey():
    config.read('parameters.config')
    p = int(config['PARAMETERS']['p'])
    g = int(config['PARAMETERS']['g'])
    pn = dh.DHParameterNumbers(p, g)
    parameters = pn.parameters()
    public_key = parameters.generate_private_key()
    return public_key
    
def clearStoredPublicKeyValue():
    config['PARAMETERS']['y'] = ""
    with open ('parameters.config', 'w') as configfile:
        config.write(configfile)   
    
def startNewCommunication():
    privateKey = generateNewPrivateKey()
    publicKey = generateNewPublicKey()
    print(publicKey.private_bytes("DER","PKCS8", "NoEncryption")) 
    

def storeParameters():
    parameters = dh.generate_parameters(generator=2, key_size=512)
    pn = parameters.parameter_numbers()
    p = pn.p
    g = pn.g
    y = 10
    config['PARAMETERS'] = {'p': p, 'g': g}
    with open ('parameters.config', 'w') as configfile:
        config.write(configfile)

def getSharedKey():
    config.read('parameters.config')
    p = int(config['PARAMETERS']['p'])
    g = int(config['PARAMETERS']['g'])
    y = int(config['PARAMETERS']['y'])
    pn = dh.DHParameterNumbers(p, g)
    peer_public_numbers = dh.DHPublicNumbers(y, pn)
    peer_public_key = peer_public_numbers.public_key()
    private_key = pn.parameters().generate_private_key()
    print("private key: " + str(private_key))
    shared_key = private_key.exchange(peer_public_key)
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data',
    ).derive(shared_key)
    return derived_key
