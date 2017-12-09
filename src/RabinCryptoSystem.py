from PrimeNumberGenerator import PrimeNumberGenerator
import utils
import time
import binascii

# for every public function:
#     every input - hex string
#     every output - hex string (except c1 and c2 in 'encrypt' function)


class RabinCryptoSystem:
    def __init__(self, key_size_bits=128):
        self._png = PrimeNumberGenerator(int(time.time()))
        self.p = 10666988503151462791  # self._png.generate_blume_prime(key_size_bits >> 1)
        self.q = 14893377444730166807  # self._png.generate_blume_prime(key_size_bits >> 1)
        self.n = self.p * self.q
        self.b = self._png.generate_number_even(bits=key_size_bits)

        self.l = utils.byte_length(self.n)
        print("p = " + str(self.p))
        print("q = " + str(self.q))
        print("n = " + str(self.n))
        hex = binascii.hexlify(self.n.to_bytes(utils.byte_length(self.n), byteorder='big'))
        print("n hex: " + str(hex))
        print("b = = " + str(self.b))

        gcd, self.u, self.v = utils.EucldeanExtended(self.p, self.q)

    def generate_key_pair(self, key_size_bits=128):
        self.p = self._png.generate_blume_prime(key_size_bits >> 1)
        self.q = self._png.generate_blume_prime(key_size_bits >> 1)
        self.n = self.p * self.q
        self.b = self._png.generate_number_even(key_size_bits)

        self.l = utils.byte_length(self.n)
        _, self.u, self.v = utils.EucldeanExtended(self.p, self.q)

        print("p = " + str(self.p))
        print("q = " + str(self.q))
        print("n = " + str(self.n))
        hex = binascii.hexlify(self.n.to_bytes(utils.byte_length(self.n), byteorder='big'))
        print("n hex: " + str(hex))
        print("b = " + str(self.b))

        return binascii.hexlify(self.n.to_bytes(utils.byte_length(self.n), byteorder='big')), binascii.hexlify(self.b.to_bytes(utils.byte_length(self.b), byteorder='big'))

    def __encode_message__(self, msg):
        encoded = bytearray()
        encoded.append(0x00)
        encoded.append(0xff)
        for i in range(self.l - 10 - len(msg)):
            encoded.append(0x00)
        for i in range(0, len(msg)):
            encoded.append(msg[i])
        for b in self._png.generate_bytes(8):
            encoded.append(b)
        return encoded

    def __decode_message__(self, msg):
        decoded = msg[1:self.l - 9]
        return decoded

    def encrypt(self, hex_msg):
        if not isinstance(hex_msg, str):
            raise ValueError("'hex_msg' must be string")
        
        msg = binascii.unhexlify(hex_msg)
        if len(msg) + 10 > self.l:
            raise ValueError("'hex_msg' must be less than " + str(self.l - 10) + " bytes")

        encoded = self.__encode_message__(msg.encode(encoding='utf-8'))
        x = int.from_bytes(encoded, byteorder='big')

        y = (x * (x + self.b)) % self.n
        c1 = ((x + (self.b >> 1)) % self.n) & 0x01
        c2 = 0x01 if utils.Jacobi((x + (self.b >> 1)), self.p, self.q) == 1 else 0x00

        result = binascii.hexlify(y.to_bytes(utils.byte_length(y), byteorder='big'))
        return result, c1, c2

    def decrypt(self, hex_y, c1, c2):
        number = int.from_bytes(binascii.unhexlify(hex_y), byteorder='big')
        for x in self.__sqrt__(number, self.b):
            if (((x + (self.b >> 1)) % self.n) & 0x01 == c1) and ((0x01 if utils.Jacobi((x + (self.b >> 1)), self.p, self.q) == 1 else 0x00) == c2):
                return binascii.hexlify(self.__decode_message__(x.to_bytes(utils.byte_length(x), byteorder='big')))

    def __sqrt__(self, y, b=0):
        y += (b * b >> 2)
        s1 = pow(y, (self.p + 1) >> 2, self.p)
        s2 = pow(y, (self.q + 1) >> 2, self.q)

        x1 = (-(b >> 1) + (self.v * self.q * s1 + self.u * self.p * s2)) % self.n
        x2 = (-(b >> 1) + (-self.v * self.q * s1 + self.u * self.p * s2)) % self.n
        x3 = (-(b >> 1) + (-self.v * self.q * s1 - self.u * self.p * s2)) % self.n
        x4 = (-(b >> 1) + (self.v * self.q * s1 - self.u * self.p * s2)) % self.n

        return x1, x2, x3, x4

    def sign(self, hex_msg):
        if not isinstance(hex_msg, str):
            raise ValueError("'hex_msg' must be hex string")

        msg = binascii.unhexlify(hex_msg)
        if len(msg) + 10 > self.l:
            raise ValueError("'hex_msg' must be less than " + str(self.l - 10) + " bytes")

        x = int.from_bytes(self.__encode_message__(msg), byteorder='big')
        while (utils.Legendre(x, self.p) != 1 or utils.Legendre(x, self.q) != 1):
            x = int.from_bytes(self.__encode_message__(msg), byteorder='big')

        s, _, _, _ = self.__sqrt__(x)
        return binascii.hexlify(s.to_bytes(utils.byte_length(s), byteorder='big'))

    def verify(self, hex_msg, hex_signature):
        s_num = int.from_bytes(binascii.unhexlify(hex_signature), byteorder='big')
        x1 = pow(s_num, 2, self.n)

        return hex_msg in str(binascii.hexlify(self.__decode_message__(x1.to_bytes(utils.byte_length(x1), byteorder='big'))))