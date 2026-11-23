
import secrets


N = 256
Q = 3329
K = 2
ETA = 3


def generate_uniform_poly():
    return [secrets.randbelow(Q) for _ in range(N)]


def generate_noise_poly(eta=ETA):

    coefficients = []

    for _ in range(N):

        random_bits = secrets.randbits(2 * eta)

        low_bits = random_bits & ((1 << eta) - 1)
        high_bits = random_bits >> eta

        coefficient = low_bits.bit_count() - high_bits.bit_count()

        coefficients.append(coefficient % Q)

    return coefficients


def poly_add(a, b):
    return [(x + y) % Q for x, y in zip(a, b)]


def poly_sub(a, b):
    return [(x - y) % Q for x, y in zip(a, b)]


def poly_mul(a, b):

    result = [0] * N

    for i in range(N):
        for j in range(N):

            degree = i + j
            product = a[i] * b[j]

            if degree < N:
                result[degree] += product
            else:
                result[degree - N] -= product

    return [value % Q for value in result]


def matrix_vector_mul(matrix, vector):

    result = []

    for row in matrix:

        polynomial_sum = [0] * N

        for polynomial, vector_poly in zip(row, vector):

            product = poly_mul(polynomial, vector_poly)

            polynomial_sum = poly_add(
                polynomial_sum, product
            )

        result.append(polynomial_sum)

    return result


def generate_matrix(k=K):

    return [
        [generate_uniform_poly() for _ in range(k)]
        for _ in range(k)
    ]


def generate_module_lwe_sample():

    A = generate_matrix()

    s = [generate_noise_poly() for _ in range(K)]
    e = [generate_noise_poly() for _ in range(K)]

    # Generate the public vector using the Module-LWE equation
    t = matrix_vector_mul(A, s)

    for i in range(K):
        t[i] = poly_add(t[i], e[i])

    return A, s, e, t


def to_centered(value):

    if value > Q // 2:
        return value - Q

    return value


def display_polynomial(poly, count=12):

    return [to_centered(value) for value in poly[:count]]


def main():

    print("=" * 55)
    print("       MODULE-LWE MATHEMATICAL DEMONSTRATION")
    print("=" * 55)

    print(f"\nPolynomial degree: {N}")
    print(f"Modulus: {Q}")
    print(f"Module dimension: {K}")
    print(f"Noise parameter: {ETA}")

    A, s, e, t = generate_module_lwe_sample()

    print("\nGenerated Module-LWE sample.")

    print("\nPublic matrix A (first polynomial):")
    print(display_polynomial(A[0][0]))

    print("\nSecret vector s (first polynomial):")
    print(display_polynomial(s[0]))

    print("\nError vector e (first polynomial):")
    print(display_polynomial(e[0]))

    print("\nPublic vector t (first polynomial):")
    print(display_polynomial(t[0]))

    # Verify the Module-LWE relationship
    reconstructed = matrix_vector_mul(A, s)

    recovered_error = [
        poly_sub(t[i], reconstructed[i])
        for i in range(K)
    ]

    print("\nVerification:")

    if recovered_error == e:
        print("SUCCESS: t = A*s + e (mod Q)")
    else:
        print("FAILURE: Module-LWE relation mismatch.")

    print("\n" + "=" * 55)


if __name__ == "__main__":
    main()
