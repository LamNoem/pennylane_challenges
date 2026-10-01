import json
import pennylane as qp
import pennylane.numpy as np

n_qubits = 9
dev = qp.device("default.qubit", wires=n_qubits)
error_dict = {0: 'PauliX', 1: 'PauliY', 2: 'PauliZ'}

def error(error_key, qubit):
    """Defines the error that is induced in the circuit.

    Args:
        error_key (int): An integer associated to the type of error (Pauli X, Y, or Z)
        qubit (int): The qubit that the error occurs on.
    """
    getattr(qp, error_dict[error_key])(qubit)

@qp.qnode(dev)
def shor(state, error_key, qubit):
    """A circuit defining Shor's code for error correction.

    Args:
        state (list(float)): The quantum state of the first qubit in the circuit.
        error_key (int): An integer associated to the type of error (Pauli X, Y, or Z)
        qubit (int): The qubit that the error occurs on.

    Returns:
        (list(float)): The expectation value of the Pauli Z operator on every qubit.
    """
    qp.StatePrep(np.array(state), wires=0)

    # Put your code here #
    qp.CNOT(wires=[0,3])
    qp.CNOT(wires=[0,6])
    qp.H(0)
    qp.H(3)
    qp.H(6)
    qp.CNOT(wires=[0,1])
    qp.CNOT(wires=[3,4])
    qp.CNOT(wires=[6,7])
    qp.CNOT(wires=[0,2])
    qp.CNOT(wires=[3,5])
    qp.CNOT(wires=[6,8])
    error(error_key,qubit)
    qp.CNOT(wires=[0,1])
    qp.CNOT(wires=[3,4])
    qp.CNOT(wires=[6,7])
    qp.CNOT(wires=[0,2])
    qp.CNOT(wires=[3,5])
    qp.CNOT(wires=[6,8])
    qp.Toffoli(wires=[2,1,0])
    qp.Toffoli(wires=[5,4,3])
    qp.Toffoli(wires=[8,7,6])
    qp.H(0)
    qp.H(3)
    qp.H(6)
    qp.CNOT(wires=[0,3])
    qp.CNOT(wires=[0,6])
    qp.Toffoli(wires=[6,3,0])
    out = []
    for i in range(9):
        out.append(qp.expval(qp.PauliZ(i)))
    return out
    
# These functions are responsible for testing the solution.
def run(test_case_input: str) -> str:
    state, error_key, qubit = json.loads(test_case_input)
    outs = [round(float(elem), 1) for elem in shor(state, error_key, qubit)]
    output = [outs[i] for i in dev.wires]

    return str(output)

def check(solution_output: str, expected_output: str) -> None:
    solution_output = json.loads(solution_output)
    expected_output = json.loads(expected_output)

    assert np.allclose(solution_output, expected_output, rtol=1e-4), "Incorrect result for expectation values."