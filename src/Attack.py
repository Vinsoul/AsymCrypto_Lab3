from RabinCryptoSystem import RabinCryptoSystem
import binascii
import utils

def ImplementAttack(hex_n):
    rcs = RabinCryptoSystem()
    rcs.n = int.from_bytes(binascii.unhexlify(hex_n), byteorder='big')
    t = rcs._png.generate_number_even(bits=1024)
    y = pow(t, 2, rcs.n)
    print("y = " + str(binascii.hexlify(y.to_bytes(utils.byte_length(y), byteorder='big'))))
    hex_z = input("Server response: ")
    z = int.from_bytes(binascii.unhexlify(hex_z), byteorder='big')
    if (z == y or z == (rcs.n - y)):
        print("Failed")
    else:
        p = utils.GCD(t + z, rcs.n)
        q = rcs.n // p
        print("p = " + str(p))
        print("q = " + str(q))
        print("p * q =  " + str(p * q))
        print("n = " + str(rcs.n))
        print (p * q == rcs.n)