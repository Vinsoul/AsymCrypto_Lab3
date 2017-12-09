import utils
from math import ceil

class PrimeNumberGenerator:
    p = 0xD5BBB96D30086EC484EBA3D7F9CAEB07
    q = 0x425D2B9BFDB25B9CF6C416CC6E37B59C1F

    n = p * q
    primes = [3, 5, 7, 11, 13, 17, 19]

    def __init__(self, seed):
        self._seed = int(seed)

    def generate_bytes(self, num_bytes):
        result = bytearray()
        for i in range(0, num_bytes):
            self._seed = pow(self._seed, 2, PrimeNumberGenerator.n)
            result.append(self._seed % 256)
        return result

    def generate_number_odd(self, bits):
        rem = bits % 8
        mask = 0xff
        if (rem != 0):
            bits += (8 - rem)
            mask = 0x01
            for i in range(rem - 1):
                mask <<= 1
                mask = mask | 0x01

        bytes = self.generate_bytes(bits >> 3)
        bytes[len(bytes) - 1] &= mask
        result = int.from_bytes(bytes, byteorder='little', signed=False)
        result = result | 0x01
        return result

    def generate_number_even(self, bits):
        result = self.generate_number_odd(bits) ^ 0x01
        return result

    def miller_rabin_test(self, p, k=100):
        # Check for small primes - sieving a lot of non-primes
        for prime in PrimeNumberGenerator.primes:
            if p % prime == 0:
                return False

        bits = p.bit_length()

        s = 0
        d = p - 1

        # p - 1 = d * 2^s
        # While d is odd
        while (d & 0x01 != 1):
            s += 1
            d >>= 1

        for i in range(k):
            x = self.generate_number_odd(bits)

            x = pow(x, d, p)
            if (x == 1):
                continue
            for r in range(s - 1):
                if (x == p - 1):
                    continue
                x = pow(x, 2, p)

            if (x == p - 1):
                continue
            else:
                return False

        return True


    def generate_prime(self, bits):
        number = self.generate_number_odd(bits)
        while (not self.miller_rabin_test(number)):
            number += 2
        return number

    def generate_blume_prime(self, bits):
        number = self.generate_number_odd(bits - 2)
        while not (self.miller_rabin_test(4 * number + 3)):
            number += 2
            while not (self.miller_rabin_test(number)):
                number += 2

        return 4 * number + 3
