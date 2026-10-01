import json
import pennylane as qp
import pennylane.numpy as np
dev = qp.device("default.qubit",wires=2)

@qp.qnode(dev)
def circuit1(angles):
    """
    A Qnode implementing the circuit shown in the top part of the image

    Args:
        angles (np.ndarray(float)): A list [theta_1, theta_2] of angle
        parameters for the RX and RY gates respectively
    
    Returns: 
        (np.tensor): The expectation value of the PauliX observable
    """

    # Put your code here #
    qp.RX(angles[0],0)
    qp.RY(angles[1],0)
        

    # Return the expectation value
    return qp.expval(qp.PauliX(0))

@qp.qnode(dev)
def circuit2(angles):
    """
    A Qnode implementing the circuit shown in the bottom part of the image

    Args:
        angles (np.ndarray(float)): A list [theta_1, theta_2] of angle
        parameters for the RX and RY gates respectively
    
    Returns: 
        (np.tensor): The expectation value of the PauliX observable
    """

    # Put your code here #
    qp.RY(angles[1],1)
    qp.RX(angles[0],1)
    # Return the expectation value
    return qp.expval(qp.PauliX(1))

def compare_circuits(angles):
    """
    Given two angles, compare two circuit outputs that have their order of
    operations flipped: RX then RY VERSUS RY then RX.

    Args:
        angles (np.ndarray(float)): An array of two angles [theta_1, theta_2]

    Returns:
        (float): The absolute value of the difference between the expectation
        values of the circuits.
    """

    # Put your code here #
    c1 = circuit1(angles)
    c2 = circuit2(angles)

    # Return the required difference in expectation values
    return abs(c1 - c2)
# These functions are responsible for testing the solution.
def run(test_case_input: str) -> str:
    ins = json.loads(test_case_input)
    output = compare_circuits(ins)

    return str(output)


def check(solution_output: str, expected_output: str) -> None:
    solution_output = json.loads(solution_output)
    expected_output = json.loads(expected_output)
    assert np.isclose(solution_output, expected_output, rtol=1e-4)