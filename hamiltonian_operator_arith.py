import json
import pennylane as qp
import pennylane.numpy as np

def hamiltonian(num_wires):
    """
    A function for creating the Hamiltonian in question for a general
    number of qubits.

    Args:
        num_wires (int): The number of qubits.

    Returns:
        (qp.Hamiltonian): A PennyLane Hamiltonian.
    """

    # Put your solution here #
    coeffs = []
    obs = []
    for j in range(num_wires):
        for i in range(j):  
            coeffs.append(1/3)
            obs.append(qp.PauliX(i) @ qp.PauliX(j))

    for i in range(num_wires-1):
            coeffs.append(-1)
            obs.append(qp.PauliZ(i))

    K = qp.Hamiltonian(coeffs,obs)
            
    return K

def expectation_value(num_wires):
    """
    Simulates the circuit in question and returns the expectation value of the 
    Hamiltonian in question.

    Args:
        num_wires (int): The number of qubits.

    Returns:
        (float): The expectation value of the Hamiltonian.
    """

    # Put your solution here #

    # Define a device using qp.device
    dev = qp.device("default.qubit", wires=num_wires)

    @qp.qnode(dev)
    def circuit(num_wires):
        """
        A quantum circuit with Hadamard gates on every qubit and that measures
        the expectation value of the Hamiltonian in question. 
        
        Args:
        	num_wires (int): The number of qubits.

		Returns:
			(float): The expectation value of the Hamiltonian.
        """

        # Put Hadamard gates here #
        for i in range(num_wires):
            qp.Hadamard(i)
        # Then return the expectation value of the Hamiltonian using qp.expval
        return qp.expval(hamiltonian(num_wires))

    return circuit(num_wires)

# These functions are responsible for testing the solution.
def run(test_case_input: str) -> str:
    num_wires = json.loads(test_case_input)
    output = expectation_value(num_wires)

    return str(output)


def check(solution_output: str, expected_output: str) -> None:
    solution_output = json.loads(solution_output)
    expected_output = json.loads(expected_output)
    assert np.allclose(solution_output, expected_output, rtol=1e-4)