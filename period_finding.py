import numpy as np
from math import gcd
from fractions import Fraction

from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import UnitaryGate, QFTGate
from qiskit_aer import AerSimulator


# Configuration
N = 15
A = 2

COUNTING_QUBITS = 4
WORK_QUBITS = 4
SHOTS = 2048


# Construct Modular Multiplication Unitary
def modular_multiplication(multiplier, modulus):

    dimension = 2 ** WORK_QUBITS
    matrix = np.zeros((dimension, dimension), dtype=complex)

    if gcd(multiplier, modulus) != 1:
        raise ValueError("Multiplier must be coprime to modulus.")

    for value in range(dimension):

        if value < modulus:
            result = (multiplier * value) % modulus
        else:
            result = value

        matrix[result, value] = 1

    return UnitaryGate(matrix, label=f"M_{multiplier}")


# Construct the Quantum Period-Finding Circuit
def create_circuit():

    circuit = QuantumCircuit(
        COUNTING_QUBITS + WORK_QUBITS,
        COUNTING_QUBITS
    )

    counting = list(range(COUNTING_QUBITS))

    work = list(
        range(COUNTING_QUBITS,
              COUNTING_QUBITS + WORK_QUBITS)
    )

    # Initialize work register to |1>
    circuit.x(work[0])

    # Create superposition in counting register
    for qubit in counting:
        circuit.h(qubit)

    # Apply controlled modular exponentiation
    for i, control in enumerate(counting):

        multiplier = pow(A, 2 ** i, N)

        if multiplier == 1:
            continue

        unitary = modular_multiplication(
            multiplier, N
        )

        controlled_unitary = unitary.control()

        circuit.append(
            controlled_unitary,
            [control] + work
        )

    # Apply inverse Quantum Fourier Transform
    inverse_qft = QFTGate(COUNTING_QUBITS).inverse()

    circuit.append(inverse_qft, counting)

    # Measure counting register
    circuit.measure(counting, range(COUNTING_QUBITS))

    return circuit


# Recover a Candidate Order from Measurement
def recover_order(measured_value):

    # Zero phase does not provide useful information
    if measured_value == 0:
        return None

    phase = measured_value / (2 ** COUNTING_QUBITS)

    # Approximate phase using continued fractions
    fraction = Fraction(phase).limit_denominator(N)

    denominator = fraction.denominator

    # Test multiples of the denominator
    for candidate in range(denominator, N + 1, denominator):

        if pow(A, candidate, N) == 1:
            return candidate

    return None


# Extract Factors Using the Recovered Order
def extract_factors(order):

    if order is None or order % 2 != 0:
        return None

    x = pow(A, order // 2, N)

    if x == N - 1:
        return None

    factor1 = gcd(x - 1, N)
    factor2 = gcd(x + 1, N)

    if 1 < factor1 < N:
        return factor1, N // factor1

    if 1 < factor2 < N:
        return factor2, N // factor2

    return None


# Main Execution
def main():

    print("=" * 55)
    print("       QUANTUM PERIOD FINDING - QISKIT")
    print("=" * 55)

    print(f"\nTarget integer N: {N}")
    print(f"Base integer A: {A}")

    # Construct circuit
    circuit = create_circuit()

    print("\nQuantum circuit constructed successfully.")

    print("\nCircuit structure:")
    print(circuit.draw(output="text"))

    # Initialize simulator
    simulator = AerSimulator()

    # Compile circuit for simulator
    compiled_circuit = transpile(
        circuit,
        simulator,
        optimization_level=1
    )

    # Execute circuit
    result = simulator.run(
        compiled_circuit,
        shots=SHOTS
    ).result()

    counts = result.get_counts()

    print("\nMeasurement Results:")
    for outcome, frequency in counts.most_common():
        print(f"{outcome}: {frequency}")

    # Analyze measurement outcomes
    print("\nRecovering multiplicative order...")

    for outcome, frequency in counts.most_common():

        measured_value = int(outcome.replace(" ", ""), 2)

        order = recover_order(measured_value)

        if order is None or order % 2 != 0:
            continue

        factors = extract_factors(order)

        if factors:

            p, q = factors

            print(f"\nRecovered order: {order}")
            print(f"Factor 1: {p}")
            print(f"Factor 2: {q}")
            print(f"Verification: {p} x {q} = {p * q}")

            break

    else:
        print("\nNo usable period found.")
        print("Try increasing the number of shots.")

    print("\n" + "=" * 55)


if __name__ == "__main__":
    main()
