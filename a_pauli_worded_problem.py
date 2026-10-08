import json
import pennylane as qp
import pennylane.numpy as np
import scipy
def abs_dist(rho, sigma):
    """A function to compute the absolute value |rho - sigma|."""
    polar = scipy.linalg.polar(rho - sigma)
    return polar[1]

def word_dist(word):
    """A function which counts the non-identity operators in a Pauli word"""
    return sum(word[i] != "I" for i in range(len(word)))


# Produce the Pauli density for a given Pauli word and apply noise

def noisy_Pauli_density(word, lmbda):
    """
       A subcircuit which prepares a density matrix (I + P)/2**n for a given Pauli
       word P, and applies depolarizing noise to each qubit. Nothing is returned.

    Args:
            word (str): A Pauli word represented as a string with characters I,  X, Y and Z.
            lmbda (float): The probability of replacing a qubit with something random.
    """

    # Put your code here #
    n = len(word)
    paulis = {
        "I": np.eye(2),
        "X": np.array([[0, 1], [1, 0]]),
        "Y": np.array([[0, -1j], [1j, 0]]),
        "Z": np.array([[1, 0], [0, -1]]),
    }

    P = paulis[word[0]]
    for op in word[1:]:
        P = np.kron(P, paulis[op])

    #notes for me: A Pauli word is a short label for an operator acting on several qubits.
    #  Each letter describes what happens to one qubit:

    # I: leave it unchanged
    # X: flip it
    # Y: flip it and add a phase
    # Z: leave 0 alone and change the sign of 1
    # For example, XIZ means apply X to the first qubit, I to the second, and Z to the third.
    #  Mathematically, that combined operator is (X \otimes I \otimes Z).

    # It’s an operator—not a density matrix yet. 
    # The code turns it into a density matrix with ((I + P)/2^n), where (P) is the matrix represented by the word and (n) is the number of qubits.
    #  For a word containing at least one non-I, this represents a mixed state in the (+1) eigenspace of (P).
    # so now we have to turn the op matrix (large matrix representing each op on a qubit) into a density matrix (large matrix representing the mixed state of each qubit). 
    rho = (np.eye(2**n) + P) / (2**n)

    qp.QubitDensityMatrix(rho, wires=range(n))
    # each qubit is depolarized independently with probability (lambda).
    for i in range(n):
        qp.DepolarizingChannel(lmbda, wires=i)
    





# Compute the trace distance from a noisy Pauli density to the maximally mixed density

def maxmix_trace_dist(word, lmbda):
    """
       A function compute the trace distance between a noisy density matrix, specified
       by a Pauli word, and the maximally mixed matrix.

    Args:
            word (str): A Pauli word represented as a string with characters I, X, Y and Z.
            lmbda (float): The probability of replacing a qubit with something random.

    Returns:
            float: The trace distance between two matrices encoding Pauli words.
    """

    # Put your code here #
    n = len(word)

    dev = qp.device("default.mixed", wires=range(n))

    @qp.qnode(dev)
    def circuit():
        noisy_Pauli_density(word, lmbda)
        return qp.state()

    noisy = circuit()

    #large 1 diagonal matrix that basically says each qubit it maxmix state. for 1 qubit: [[0.5, 0], [0, 0.5]], for 2 qubits: [[0.25, 0, 0, 0], [0, 0.25, 0, 0], [0, 0, 0.25, 0], [0, 0, 0, 0.25]],
    max_mix = np.eye(2**n) / (2**n)

    absolute_dist = abs_dist(noisy, max_mix)

    trace_distance = 0.5 * np.trace(absolute_dist)

    return trace_distance

def bound_verifier(word, lmbda):
    """
       A simple check function which verifies the trace distance from a noisy Pauli density
       to the maximally mixed matrix is bounded by (1 - lambda)^|P|.

    Args:
            word (str): A Pauli word represented as a string with characters I, X, Y and Z.
            lmbda (float): The probability of replacing a qubit with something random.

    Returns:
            float: The difference between (1 - lambda)^|P| and T(rho_P(lambda), rho_0).
    """

    # Put your code here #
    non_identity_ops = word_dist(word)

    return abs((1-lmbda)**non_identity_ops - maxmix_trace_dist(word, lmbda))

# These functions are responsible for testing the solution.
def run(test_case_input: str) -> str:

    word, lmbda = json.loads(test_case_input)
    output = np.real(bound_verifier(word, lmbda))

    return str(output)


def check(solution_output: str, expected_output: str) -> None:

    solution_output = json.loads(solution_output)
    expected_output = json.loads(expected_output)
    assert np.allclose(
        solution_output, expected_output, rtol=1e-4
    ), "Your trace distance isn't quite right!"

# These are the public test cases
test_cases = [
    ('["XXI", 0.7]', '0.0877777777777777'),
    ('["XXIZ", 0.1]', '0.4035185185185055'),
    ('["YIZ", 0.3]', '0.30999999999999284'),
    ('["ZZZZZZZXXX", 0.1]', '0.22914458207245006')
]
# This will run the public test cases locally
for i, (input_, expected_output) in enumerate(test_cases):
    print(f"Running test case {i} with input '{input_}'...")

    try:
        output = run(input_)

    except Exception as exc:
        print(f"Runtime Error. {exc}")

    else:
        if message := check(output, expected_output):
            print(f"Wrong Answer. Have: '{output}'. Want: '{expected_output}'.")

        else:
            print("Correct!")


