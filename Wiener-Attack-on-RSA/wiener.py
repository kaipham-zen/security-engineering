import gmpy2
from gmpy2 import mpz

def continued_fraction(e,n):
    """Convert fraction e/n to [a0,a1,a2,...,ak]"""
    cf = []
    while n != 0:
        # Quotient of division e/n
        q = e // n
        # Append quotient to continued fraction list
        cf.append(q)
        e, n = n, e%n
    return cf

def convergents(cf):
    """Iterate over each convergent"""
    # Two lists for numerators and denominators
    num = [1, cf[0]]
    den = [0, 1]
    
    # Calculating successive convergents using Fundamental recurrence formulas
    for i in range(2, len(cf) + 1):
        num.append(cf[i-1] * num[i-1] + num[i-2])
        den.append(cf[i-1] * den[i-1] + den[i-2])
        
    # List of successive convergents in pairs of numerators and denominators (num[i],den[i])
    convergents_list = []
    for i in range(1,len(num)):
        convergents_list.append((num[i],den[i]))

    return convergents_list

def wiener_attack(e, n):
    """ Conducting wiener attack"""
    # Find continued fraction
    cf = continued_fraction(e, n)
    # Check all convergents where k is numerator, d is denominator
    for k, d in convergents(cf):
        # Check if k and d meet the requirements (d is odd, ed mod k = 1, k != 0)
        if k == 0 or e * d % k != 1 or d % 2 == 0:
            continue
        
        phi = (e * d - 1) // k
        
        # Solving quadratic equation x**2 - (p+q)x + pq = 0
        ## p+q = n - phi + 1; pq = n
        s = n - phi + 1
        
        discriminant = s**2 - 4*n
        if discriminant < 0:
            continue
        
        ## x = [-b +- isqrt(b^2-4ac)]/2a
        root = gmpy2.isqrt(discriminant)
        p = (s + root) // 2
        q = (s - root) // 2

        # Check correctness of p, q
        if p * q == n:
            return mpz(d), mpz(p), mpz(q)
    
    return None, None, None

def int_to_ascii(decrypted_int):
    """ Convert integer to ASCII representation """
    # Convert decrypted message into binary
    pt_in_binary = bin(decrypted_int)[2:]

    # Padding zeros
    padding = (8 - len(pt_in_binary) % 8) % 8
    pt_in_binary = '0' * padding + pt_in_binary
    
    pt = ""
    for i in range(0, len(pt_in_binary), 8):
        # Read 8 bits each iteration
        byte = pt_in_binary[i:i+8]
        # Convert binary to decimal
        char_code = int(byte, 2)
        # Convert decimal to ASCII and concatenate to plaintext result
        pt += chr(char_code)
    
    return pt

def main():
    e = mpz(831225867969522876916055775054661128782421970114471980281522740420874996000135337976135915389030984285006903579947506374139928919464917071723629444477004859236188084581877860467590274275760951897229141)
    n = mpz(1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000026730000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000801)
    c = mpz(147168318904755482244507140257155655972331150713367204965991168469089624675898514403145851330242392460561965612645978235388137188852360042473868876452698888814545363063985639145385098838552091801590614)

    # Question 1i
    print("\ni) Wiener's attack: ")
    d, p, q = wiener_attack(e, n)
    print(f"d = {mpz(d)}")
    print(f"p = {mpz(p)}")
    print(f"q = {mpz(q)}")

    # Question 1ii
    decrypted_int= pow(c, d, n)
    print(f"\nii) Decrypt into integer: {decrypted_int}")
        
    # Question 1iii
    pt = int_to_ascii(decrypted_int)
    print(f"\niii) Human-readable plaintext: {pt}")

if __name__ == "__main__":
    main()