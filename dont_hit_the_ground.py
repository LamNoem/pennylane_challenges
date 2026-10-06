import json
import pennylane as qp
import pennylane.numpy as np
def half_life(gamma, p):
    """Calculates the relaxation half-life of a quantum system that exchanges energy with its environment.
    This process is modeled via Generalized Amplitude Damping.

    Args:
        gamma (float): 
            The probability per unit time of the system losing a quantum of energy
            to the environment.
        p (float): The de-excitation probability due to environmental effect

    Returns:
        (float): The relaxation haf-life of the system, as explained in the problem statement.
    """

    num_wires = 1

    dev = qp.device("default.mixed", wires=num_wires)

    # Put your code here
    delta = 0.1
    steps = 1

    prob_1 = 0.5

    @qp.qnode(dev)
    def GAD(steps, gamma, p):
        for _ in range(steps):
            qp.GeneralizedAmplitudeDamping(gamma*delta, p, wires = 0)
        

        return qp.density_matrix(wires=[0])
        

    while(True):
        
        # out = GAD(steps,gamma,p)
        prob_1 = prob_1 * (1 - gamma * delta) + p * gamma * delta
        
        # prob_1 = np.real(out[1, 1])
    
        if prob_1 <= 0.25: 
            break
        steps += 1

    return steps*delta

        

# These functions are responsible for testing the solution.
def run(test_case_input: str) -> str:

    ins = json.loads(test_case_input)
    output = half_life(*ins)

    return str(output)

def check(solution_output: str, expected_output: str) -> None:
    solution_output = json.loads(solution_output)
    expected_output = json.loads(expected_output)
    assert np.allclose(
        solution_output, expected_output, atol=2e-1
    ), "The relaxation half-life is not quite right."

# These are the public test cases
test_cases = [
    ('[0.1,0.08]', '9.00'),
    ('[0.2,0.17]', '7.05')
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

#using pennylane function timed out, 
# using the math , guessed the right initial probability (based on the initial state, 50/50 superposition or start at ket(1))