from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import serialization
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


#p is prime modulo, g is generator, y is public value that is recieved, and x is private value that is sent.
p = "" #prime modulo, unchanging
g = "" #generator, unchanging
y = "" #public value, recieved from other party
x = "" #private value, kept secret
yPrivate = "" #y value for the pair containing our private key, used to recompute private key

#tmp.public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo)

def getParamsFromFile():
    """update the global variables with what is stored in config file"""
    config.read('parameters.config')
    global p, g, y, x, yPrivate
    p = int(config['PARAMETERS']['p'])
    g = int(config['PARAMETERS']['g'])
    y = int(config['PARAMETERS']['y'])
    x = int(config['PARAMETERS']['x'])
    yPrivate = int(config['PARAMETERS']['yPrivate'])

def storeParamsToFile():
    """store global variables to config file"""
    config['PARAMETERS'] = {'p': p, 'g': g, 'y': y, 'x': x, 'yPrivate': yPrivate}
    with open ('parameters.config', 'w') as configfile:
        config.write(configfile)    

def startNewCommunication():
    """load params from file, then generate new private+ public key pair
    then save configuration variables and export public key to share with other instance"""
    getParamsFromFile()
    pn = dh.DHParameterNumbers(p, g).parameters()
    privateKey = pn.generate_private_key()
    publicKey = privateKey.public_key()
    global x, y, yPrivate
    x = privateKey.private_numbers().x
    y = ""
    yPrivate = publicKey.public_numbers().y
    return publicKey

def receiveExternalKey(extKey):
    """load other party's public key, save config variable for that key, then compute session key"""
    global y
    y = extKey.public_numbers().y
    privateKey = dh.DHPrivateNumbers(x, dh.DHPublicNumbers(yPrivate, dh.DHParameterNumbers(p, g))).private_key()
    sharedKeyInit = privateKey.exchange(extKey)
    sharedKeyFinal = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data',
    ).derive(sharedKeyInit)
    return sharedKeyFinal

def resumeCommunicationSession():
    getParamsFromFile()
    privateKey = dh.DHPrivateNumbers(x, dh.DHPublicNumbers(yPrivate, dh.DHParameterNumbers(p, g))).private_key()
    publicKey = dh.DHPublicNumbers(y, dh.DHParameterNumbers(p, g)).public_key()
    sharedKeyInit = privateKey.exchange(publicKey)
    sharedKeyFinal = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data',
    ).derive(sharedKeyInit)
    return sharedKeyFinal

"""
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
"""    

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
