from PrimeNumberGenerator import PrimeNumberGenerator
from RabinCryptoSystem import RabinCryptoSystem
import time
import timeit
import utils
import binascii
import Attack

rcs = RabinCryptoSystem()
'''
msg = "sajasgdfashgdasfhdgashdagsjdagsjdagsjdgajdgajdgjdgjadsgasdghasgdyudwfav".encode(encoding='ascii')
print(binascii.hexlify(rcs.n.to_bytes(utils.byte_length(rcs.n), byteorder='big')))

encoded = rcs.encode_message(msg)
decoded = rcs.decode_message(encoded)
print("encoded: " + str(encoded))
print("decoded: " + str(decoded, encoding='ascii'))

encrypted, c1, c2 = rcs.encrypt(msg)
decrypted = rcs.decrypt(encrypted, c1, c2)
print("encrypted: " + str(encrypted))
print("decrypted: " + str(decrypted))
print("decrypted: " + str(decrypted, encoding='ascii'))
'''

'''
signature = rcs.sign("hi".encode(encoding='ascii'))
print(rcs.verify("hi".encode(encoding='ascii'), signature))


'''

'''
for i in range(0, 100):
    hex_str = "facc0fff"
    signature = rcs.sign(hex_str)
    print("signature: " + str(signature))
    print(rcs.verify(hex_str, signature))
    if not rcs.verify(hex_str, signature):
        print("Oops");

rcs.n = int.from_bytes(binascii.unhexlify("8AF55BD744C488291E1D4DE1B085A3A9"), byteorder='big')
print(rcs.verify("facc0fff", "40DED7F65B512CE7F2C4A3800C6B4AE5"))
'''

Attack.ImplementAttack("9A82B5BAD7E78687D4B8C62192A5434309B30F7DE49797DB8D590B59D3B998217B8B824A0A03AE39EB1E481E4A4AFD458FED543EAD9CE7F8659CF2592D9FD568191CCD4CD19E71DB419A10700D8E819896DC7F3B3230B3489BB879880FE5BD61C00580F15E76CC5DA8F643857152681A62D42BE474FC80B75E27885614FA2424EADC20DDF62A7E91C33E39EB1BEA5E77BACD452FD74817B02A4D283B1148C4CE64C03E456C1A79FB3B1BA7AA3555D0908969D22C589D56E4CCF5E396D41382FBEDBB73DAE1361DCB3E85FC8104CE8C160EB2E45495B358397F7622D6F4306FCE17FACDA41CBED599DC03A5D093036AC9C45C13ABDBACA3386AA06DD92ED9B2A9")
