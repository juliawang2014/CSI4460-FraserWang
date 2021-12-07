from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import serialization
import configparser

config = configparser.ConfigParser()

p = None #prime modulo, unchanging
g = None #generator, unchanging
y = None #public value, recieved from other party
x = None #private value, kept secret
yPrivate = None #y value for the pair containing our private key, used to recompute private key

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
    return publicKey.public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo)

def receiveExternalKey(extKeyBytes):
    """load other party's public key, save config variable for that key, then compute+return session key"""
    extKey = serialization.load_pem_public_key(extKeyBytes)
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
    storeParamsToFile()
    return sharedKeyFinal

def resumeCommunicationSession():
    """load parameters from file and return the resulting shared key"""
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
