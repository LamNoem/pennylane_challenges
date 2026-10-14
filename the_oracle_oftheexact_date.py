import json
import pennylane as qp
import pennylane.numpy as np
wires_m = [0, 1, 2]  # qubits needed to encode m
wires_n = [3, 4, 5]  # qubits needed to encode n
wires_aux = [6, 7, 8, 9, 10]  # auxiliary qubits you can use

# Put your code here #

# Create all the helper functions you need here

def oracle_distance(d):
    """
    Args:
        d (int): the distance with which we will check that the oracle is working properly.

    This function does not return anything, it is a quantum function that applies
    necessary gates that implement the requested oracle.

    """

    # Put your code here
    bits = 3
    for m in range(8):
        for n in range(8):
            if abs(m -n )== d:
                binary_list_m = [(m >> i) & 1 for i in reversed(range(bits))]
                # binary_list_m = reversed(binary_list_m)

                binary_list_n = [(n >> i) & 1 for i in reversed(range(bits))]
                # binary_list_n = reversed(binary_list_n)

                qp.MultiControlledX(wires = wires_m + wires_n + [wires_aux[0]], control_values = binary_list_m + binary_list_n)
                # qp.MultiControlledX(wires = wires_m + wires_n + [wires_aux[0]], control_values = binary_list_n + binary_list_m)

                qp.Z(wires=wires_aux[0])

                qp.MultiControlledX(wires = wires_m + wires_n + [wires_aux[0]], control_values = binary_list_m + binary_list_n)
                # qp.MultiControlledX(wires = wires_m + wires_n + [wires_aux[0]], control_values = binary_list_n + binary_list_m)

                

# These functions are responsible for testing the solution.
wires_m = [0, 1, 2]
wires_n = [3, 4, 5]
wires_aux = [6, 7, 8, 9, 10]

dev = qp.device("default.qubit", wires=11)


@qp.qnode(dev)
def circuit(m, n, d):
    qp.BasisEmbedding(m, wires=wires_m)
    qp.BasisEmbedding(n, wires=wires_n)
    oracle_distance(d)
    return qp.state()


def run(test_case_input: str) -> str:
    outputs = []
    d = int(json.loads(test_case_input))
    for n in range(8):
        for m in range(8):
            outputs.append(sum(circuit(n, m, d)).real)
    output_list = [round(float(elem)) for elem in outputs]
    return str(output_list)


def check(solution_output: str, expected_output: str) -> None:
    i = 0
    solution_output = json.loads(solution_output)
    expected_output = json.loads(expected_output)

    assert np.allclose(solution_output, expected_output)

    names = list(qp.specs(circuit)(np.random.randint(7), np.random.randint(7), np.random.randint(7))['resources'].gate_types.keys())

    assert names.count("QubitUnitary") == 0, "Can't use custom-built gates!"

# These are the public test cases
test_cases = [
    ('0', '[-1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, -1]'),
    ('1', '[1, -1, 1, 1, 1, 1, 1, 1, -1, 1, -1, 1, 1, 1, 1, 1, 1, -1, 1, -1, 1, 1, 1, 1, 1, 1, -1, 1, -1, 1, 1, 1, 1, 1, 1, -1, 1, -1, 1, 1, 1, 1, 1, 1, -1, 1, -1, 1, 1, 1, 1, 1, 1, -1, 1, -1, 1, 1, 1, 1, 1, 1, -1, 1]'),
    ('2', '[1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, -1, 1, 1, 1, -1, 1, 1, 1, 1, -1, 1, 1, 1, -1, 1, 1, 1, 1, -1, 1, 1, 1, -1, 1, 1, 1, 1, -1, 1, 1, 1, -1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1]'),
    ('3', '[1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, -1, 1, 1, 1, 1, 1, -1, 1, 1, -1, 1, 1, 1, 1, 1, -1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1]'),
    ('4', '[1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1]'),
    ('5', '[1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1]'),
    ('6', '[1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1]'),
    ('7', '[1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1]')
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