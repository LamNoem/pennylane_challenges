import json
import pennylane as qp
import pennylane.numpy as np

def circuit_left():
    """
    This function corresponds to the circuit on the left-hand side of the diagram in the 
    description. Simply place the necessary operations, you do not have to return anything.
    """
    #encode
    qp.CNOT(wires=[0,1])
    qp.CNOT(wires=[1,2])
    
    

def circuit_right():
    """
    This function corresponds to the circuit on the right-hand side of the diagram in the 
    description. Simply place the necessary operations, you do not have to return anything.
    """
    #decode to syndrome
    qp.CNOT(wires=[1,0])
    qp.CNOT(wires=[2,1])
    


    
    
    # Flip q2 only for syndrome q0=0, q1=1.
    qp.PauliX(wires=0)       # Convert negative control to positive.
    
    # Toffoli with controls 0,1 and target 2
    qp.Hadamard(wires=2)
    qp.CNOT(wires=[1, 2])
    qp.adjoint(qp.T)(wires=2)
    
    # Equivalent to CNOT(0 -> 2), routed through qubit 1
    qp.SWAP(wires=[0, 1])
    qp.CNOT(wires=[1, 2])
    qp.SWAP(wires=[0, 1])
    
    qp.T(wires=2)
    qp.CNOT(wires=[1, 2])
    qp.adjoint(qp.T)(wires=2)
    
    # Equivalent to CNOT(0 -> 2), routed through qubit 1
    qp.SWAP(wires=[0, 1])
    qp.CNOT(wires=[1, 2])
    qp.SWAP(wires=[0, 1])
    
    qp.T(wires=1)
    qp.T(wires=2)
    qp.Hadamard(wires=2)

    qp.CNOT(wires=[0, 1])
    qp.T(wires=0)
    qp.adjoint(qp.T)(wires=1)
    qp.CNOT(wires=[0, 1])


    # qp.ctrl(qp.PauliX, control=[0, 1], control_values=[0, 1])(2)

def U():
    """This operator generates a PauliX gate on a random qubit"""
    qp.PauliX(wires=np.random.randint(3))


dev = qp.device("default.qubit", wires=3)

@qp.qnode(dev)
def circuit(alpha, beta, gamma):
    """Total circuit joining each block.

    Args: 
        alpha (float): The first parameter of a U3 gate.
        beta (float):The second parameter of a U3 gate. 
        gamma (float): The third parameter of a U3 gate. 
    
    Returns:
        (float): The expectation value of an observable.
    """
    qp.U3(alpha, beta, gamma, wires=0)
    circuit_left()
    U()
    circuit_right()

    # Here we are returning the expected value with respect to any observable,
    # the choice of observable is not important in this exercise.

    return qp.expval(0.5 * qp.PauliZ(2) - qp.PauliY(2))

# These functions are responsible for testing the solution.
def run(test_case_input: str) -> str:
    angles = json.loads(test_case_input)
    output = circuit(*angles)
    return str(output)

def check(solution_output: str, expected_output: str) -> None:

    solution_output = json.loads(solution_output)
    expected_output = json.loads(expected_output)
    assert np.allclose(
        solution_output, expected_output, rtol=1e-4
    ), "The expected output is not quite right."

    tape = qp.workflow.construct_tape(circuit)(2.0, 1.0, 3.0)
    ops = tape.operations

    for op in ops:
        assert not (0 in op.wires and 2 in op.wires), "Invalid connection between qubits."

    assert tape.observables[0].wires == qp.wires.Wires(2), "Measurement on wrong qubit."