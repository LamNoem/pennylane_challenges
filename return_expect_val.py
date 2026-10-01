import json
import pennylane as qp
import pennylane.numpy as np
## Step 1: initialize a device
dev = qp.device("default.qubit",wires=1)

# Step 2: Add a decorator below
@qp.qnode(dev)
def simple_circuit(angle):

    """
    In this function:
        * Rotate the qubit around the y-axis by angle
        * Measure the expectation value of the Pauli X observable

    Args:
        angle (float): how much to rotate a state around the y-axis

    Returns:
        Union[tensor, float]: The expectation value of the Pauli X observable
    """
    

    # Step 3: Add gates to the QNode

    # Put your code here #
    qp.RY(angle,wires=0)

    # Step 4: Return the required expectation value 
    return qp.expval(qp.PauliX(0))

# These functions are responsible for testing the solution.
def run(test_case_input: str) -> str:
    angle = json.loads(test_case_input)
    output = simple_circuit(angle)

    return str(output)

def check(solution_output: str, expected_output: str) -> None:
    solution_output = json.loads(solution_output)
    expected_output = json.loads(expected_output)
    assert np.allclose(solution_output, expected_output, rtol=1e-4)