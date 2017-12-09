def GCD(a, b):
    while (b != 0):
        a, b = b, a % b
    return a

def EucldeanExtended(a, b):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b != 0:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0

def Legendre(x, p):
    gcd = GCD(x, p)
    if (gcd == x) or (gcd == p):
        return 0

    multiplier = 1
    while (x != 1):
        outer_break = False
        while (x & 0x01 == 0):
            x >>= 1
            multiplier *= ((-1) ** ((p * p - 1) >> 3))
            if (x == 1):
                outer_break = True

        if (outer_break):
            break
        multiplier *= (-1) ** (((x - 1) >> 1) * ((p - 1) >> 1))
        x, p = p % x, x

    if (x == 1):
        return multiplier
    if (x == 2):
        return multiplier * ((-1) ** ((p * p - 1) >> 3))
    return 0

def Jacobi(x, p, q):
    return Legendre(x, p) * Legendre(x, q)

def byte_length(number):
    bits = number.bit_length()
    rem = bits % 8
    if (rem != 0):
        return (bits >> 3) + 1
    return bits >> 3