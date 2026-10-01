import json
import pennylane as qp
import pennylane.numpy as np
# Step 1: initialize a device by the name dev
dev = qp.device("default.qubit",wires=2)
# Step 2: Add a decorator below
@qp.qnode(dev)
def simple_circuit(angle):

    """
    In this function:
        * Prepare the Bell state |Phi+>.
        * Rotate the first qubit around the y-axis by angle
        * Measure the tensor product observable Z0xZ1.

    Args:
        angle (float): how much to rotate a state around the y-axis.

    Returns:
        Union[tensor, float]: the expectation value of the Z0xZ1 observable.
    """
    

    # Step 3: Add gates to the QNode
    qp.H(0)
    qp.CNOT(wires=[0,1])
    qp.RY(angle,0)

    # Put your code here #

    # Step 4: Return the required expectation value  
    return qp.expval(qp.PauliZ(0) @ qp.PauliZ(1))

# These functions are responsible for testing the solution.
def run(test_case_input: str) -> str:
    angle = json.loads(test_case_input)
    output = simple_circuit(angle)

    return str(output)

def check(solution_output: str, expected_output: str) -> None:
    solution_output = json.loads(solution_output)
    expected_output = json.loads(expected_output)
    assert np.allclose(solution_output, expected_output, rtol=1e-4), "Not the right expectation value"