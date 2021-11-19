import diffieHellman.diffieHellman as diffieHellman
import encryption.AES as AES
import perlinNoise.perlinNoise as perlinNoise

a, b = diffieHellman.dhSend()
print(diffieHellman.dhReceive(a, b))