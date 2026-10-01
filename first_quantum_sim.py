import json
import numpy as np

def initialize_state():
    """
    Prepare a qubit in state |0>.

    Returns:
        array[float]: the vector representation of state |0>.
    """

    # PREPARE THE STATE |0>
    state = np.array([1,0])
    return state
def apply_u(U, state):
    """
    Apply the quantum operation U on the state

    Args:
        U (np.array(array(complex))): A (2,2) numpy array with complex entries 
        representing a unitary matrix.
        state (np.array(complex)): A (2,) numpy array with complex entries 
        representing a quantum state.
    
    Returns:
        (np.array(complex)): The state vector after applying U to state.
    """

    # Put your code here #
    return U @ state
def measure_state(state, num_meas):
    """
    Measure a quantum state num_meas times.

    Args:
        state (np.array(complex)): A (2,) numpy array with complex entries
        representing a quantum state.
        num_meas(float): The number of computational basis measurements on state.
        
    Returns:
        (np.array(int)) A (num_meas,) numpy array of zeros and ones, representing
        measurement outcomes on the state
    """

    # Your code here #
    probs = [0,0]
    probs[0] = abs(state[0])**2
    probs[1] = abs(state[1])**2

    measurement_basis = [0,1]
    outcome = np.random.choice(measurement_basis, int(num_meas), p=probs)
    return outcome

def quantum_algorithm(U):
    """
    Use the functions above to implement the quantum algorithm described above.

    Try and do so using three lines of code or less!

    Args:
        U (np.array(array(complex))): A (2,2) numpy array with complex entries
        representing a unitary matrix.

    Returns:
        np.array(int): the measurement results after running the algorithm 20 times
    """

    # PREPARE THE STATE, APPLY U, THEN TAKE 20 MEASUREMENT SAMPLES
    state = initialize_state()
    state = apply_u(U,state)
    outcome = measure_state(state,20)
    return outcome

# These functions are responsible for testing the solution.
def run(test_case_input: str) -> str:
    np.random.seed(0)
    ins = json.loads(test_case_input)
    output = quantum_algorithm(ins).tolist()
    return str(output)


def check(solution_output: str, expected_output: str) -> None:
    
    solution_output = json.loads(solution_output)
    expected_output = json.loads(expected_output)
    
    initial_state = initialize_state()

    assert isinstance(
        initial_state, np.ndarray
    ), "The output of your initialize_state function should be a numpy array"

    assert np.allclose(
        initial_state, np.array([1, 0])
    ), "The output of your initialize_state function isn't quite right"

    U_test = [[0.70710678, 0.70710678], [0.70710678, -0.70710678]]

    assert np.allclose(
        apply_u(U_test, np.array([1, 0])), [0.70710678, 0.70710678]
    ), "Your output of apply_u isn't quite right"

    sample_list = measure_state([0.70710678, 0.70710678], 100).tolist()

    assert (
        sample_list.count(0) + sample_list.count(1) == 100
    ), "Your measure_state function isn't quite right"

    sample_list_2 = quantum_algorithm(U_test).tolist()

    assert (
        sample_list_2.count(0) + sample_list_2.count(1) == 20
    ), "Your quantum_algorithm function isn't quite right"
    
    assert np.allclose(solution_output, expected_output)