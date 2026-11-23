
import secrets
from math import gcd


# finding the multiplicative order
def find_order(a, N):

    value = 1

    for r in range(1, N + 1):

        value = (value * a) % N

        if value == 1:
            return r

    return None


# extracting factors using the multiplicative order
def find_factors(a, r, N):

    # ensuring order is even
    if r is None or r % 2 != 0:
        return None

    # calculating a^(r/2) mod N
    x = pow(a, r // 2, N)

    # checking if x is congruent to -1 mod N
    if x == N - 1:
        return None

    # calculating potential factors
    p = gcd(x - 1, N)
    q = gcd(x + 1, N)

    # checking for non-trivial factors
    if 1 < p < N and 1 < q < N:
        return p, q

    return None


# Shor's Factorization Algorithm
def shors_algorithm(N, max_attempts=100):

    if N < 2:
        raise ValueError("N must be greater than 1.")

    print(f"\nAttempting to factorize N = {N}")

    # handling even numbers directly
    if N % 2 == 0:
        return 2, N // 2

    # handling prime numbers
    for divisor in range(3, int(N ** 0.5) + 1, 2):
        if N % divisor == 0:
            break
    else:
        return None

    # Looping until valid factors are found
    for attempt in range(1, max_attempts + 1):

        print(f"\nAttempt {attempt}")

        # selecting a random integer
        a = secrets.randbelow(N - 3) + 2

        print(f"Selected base a = {a}")

        # calculating GCD for a,N
        common_factor = gcd(a, N)

        if common_factor > 1:
            print("Non-trivial factor found directly using GCD.")
            return common_factor, N // common_factor

        # finding the multiplicative order
        r = find_order(a, N)

        print(f"Multiplicative order r = {r}")

        # extracting factors
        factors = find_factors(a, r, N)

        if factors:
            return factors

        print("Unsuccessful attempt. Trying another base.")

    return None


# Main Function
def main():

    print("=" * 50)
    print("       SHOR'S FACTORIZATION ALGORITHM")
    print("=" * 50)

    N = int(input("\nEnter a composite integer: "))

    factors = shors_algorithm(N)

    if factors:

        p, q = factors

        print("\nFactorization Successful!")
        print(f"Factor 1: {p}")
        print(f"Factor 2: {q}")
        print(f"Verification: {p} x {q} = {p * q}")

    else:
        print("\nNo non-trivial factors found.")
        print("The input may be prime or attempts were unsuccessful.")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
