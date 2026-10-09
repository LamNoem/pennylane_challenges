import json
import pennylane as qp
import pennylane.numpy as np
dev = qp.device("default.qubit", wires=5)


@qp.qnode(dev)
def evolve_state(coeffs, time):
    """
    Args:
        coeffs (list(float)): A list of the coupling constants g_1, g_2, g_3, and g_4
        time (float): The evolution time of th system under the given Hamiltonian

    Returns:
        (numpy.tensor): The density matrix for the evolved state of the central spin.
    """

    # We build the Hamiltonian for you

    operators = [
        qp.PauliZ(0) @ qp.PauliZ(1),
        qp.PauliZ(0) @ qp.PauliZ(2),
        qp.PauliZ(0) @ qp.PauliZ(3),
        qp.PauliZ(0) @ qp.PauliZ(4),
    ]
    hamiltonian = qp.dot(coeffs, operators)

    # Put your code here #
    #state prep
    qp.Hadamard(wires=0)
    raw_alphas = np.array([np.cos(0.4/2), np.sin(0.4/2)], dtype=complex)
    state_vector = raw_alphas / np.linalg.norm(raw_alphas)
    qp.StatePrep(state_vector, wires=[1])
    raw_alphas = np.array([np.cos(1.2/2), np.sin(1.2/2)], dtype=complex)
    state_vector = raw_alphas / np.linalg.norm(raw_alphas)
    qp.StatePrep(state_vector, wires=[2])
    raw_alphas = np.array([np.cos(1.8/2), np.sin(1.8/2)], dtype=complex)
    state_vector = raw_alphas / np.linalg.norm(raw_alphas)
    qp.StatePrep(state_vector, wires=[3])
    raw_alphas = np.array([np.cos(0.6/2), np.sin(0.6/2)], dtype=complex)
    state_vector = raw_alphas / np.linalg.norm(raw_alphas)
    qp.StatePrep(state_vector, wires=[4])

    # state evolves under hamil. over time
    qp.evolve(hamiltonian, time)
    # Return the required density matrix.
    return qp.density_matrix(wires=[0])

def purity(rho):
    """
    Args:
        rho (array(array(complex))): An array-like object representing a density matrix

    Returns:
        (float): The purity of the density matrix rho

    """

    # Put your code here
    # The purity of a density matrix ρ is a scalar quantity defined as the trace of its square,
    # \(\gamma \equiv \operatorname{tr}(\rho^2)\), 
    # which measures whether a quantum state is pure or mixed
    # Return the purity
    return float(np.real(np.trace(rho @ rho)))

def recoherence_time(coeffs):
    """
    Args:
        coeffs (list(float)): A list of the coupling constants g_1, g_2, g_3, and g_4.

    Returns:
        (float): The recoherence time of the central spin.

    """

    # Return the recoherence time
    time = 0.0
    pur = 0.0
    has_decohered = False
    while True: # could do within a tolerance
        time += 0.002
        density = evolve_state(coeffs, time)
        pur = purity(density)

        if pur < 0.95:
            has_decohered = True

        if has_decohered and np.isclose(pur, 1.0, atol=1e-4):
            return time


        
        

# These functions are responsible for testing the solution.
def run(test_case_input: str) -> str:
    params = json.loads(test_case_input)
    output = recoherence_time(params)

    return str(output)


def check(solution_output: str, expected_output: str) -> None:
    solution_output = json.loads(solution_output)
    expected_output = json.loads(expected_output)

    assert np.isclose(solution_output, expected_output, rtol=5e-2)

# These are the public test cases
test_cases = [
    ('[5,5,5,5]', '0.314'),
    ('[1.1,1.3,1,2.3]', '15.71')
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