import json
import pennylane as qp
import pennylane.numpy as np

# Step 1: initialize a device
dev = qp.device("default.qubit",wires=1)

# Step 2: Add a decorator below
@qp.qnode(dev)
def simple_circuit(angle):
    """
    In this function:
        * Rotate the qubit around the x-axis by angle.
        * Measure the probability the qubit is in the zero state.

    Args:
        angle (float): how much to rotate a state around the x-axis.

    Returns:
        np.array(float): the probability of of the state being in the 0
        ground state.
    """
    

    # Step 3: Add gates to the QNode
    qp.RX(angle,0)
    # Put your code here #

    # Step 4: Return the required probability  
    return qp.probs(0)
# These functions are responsible for testing the solution.
def run(test_case_input: str) -> str:
    angle = json.loads(test_case_input)
    output = simple_circuit(angle)[0]

    return str(output)


def check(solution_output: str, expected_output: str) -> None:
    solution_output = json.loads(solution_output)
    expected_output = json.loads(expected_output)
    assert np.allclose(solution_output, expected_output, rtol=1e-4)