import json
import pennylane as qp
import pennylane.numpy as np
def zenda_operator():
    """
    Quantum function corresponding to the operator to be applied by
    Zenda in her qubits.This function does not return anything, 
    you must simply write the necessary gates.
    """

    # Put your code here #
    qp.CNOT(wires=["z0", "z1"])
def reece_operator():
    """
    Quantum function corresponding to the operator to be applied by
    Reece in his qubits.This function does not return anything, 
    you must simply write the necessary gates.
    """

    # Put your code here #
    qp.CZ(wires=["r0", "r1"])
def magic_operator():
    """
    Quantum function corresponding to the operator to be applied on the "z1"
    and "r1" qubits. This function does not return anything, you must
    simply write the necessary gates.

    """

    # Put your code here #
    qp.CNOT(wires=["z1", "r1"])
    qp.Hadamard(wires=["z1"])
    qp.CZ(wires=["r1", "z1"])
def bell_generator():
    """
    Quantum function preparing bell state shared by Reece and Zenda.
    """

    qp.Hadamard(wires=["z1"])
    qp.CNOT(wires=["z1", "r1"])


dev = qp.device("default.qubit", wires=["z0", "z1", "r1", "r0"])

@qp.qnode(dev)
def circuit(j, k):
    bell_generator()

    # j encoding and Zenda operation
    qp.BasisEmbedding([j], wires="z0")
    zenda_operator()

    # k encoding and Reece operation
    qp.BasisEmbedding([k], wires="r0")
    reece_operator()

    magic_operator()

    return qp.probs(wires=dev.wires)

# These functions are responsible for testing the solution.
def run(test_case_input: str) -> str:
    return None


def check(solution_output: str, expected_output: str) -> None:

    try:
        dev1 = qp.device("default.qubit", wires = ["z0", "z1"])
        @qp.qnode(dev1)
        def circuit1():
            zenda_operator()
            return qp.probs(dev1.wires)
        circuit1()
    except:
        assert False, "zenda_operator can only act on z0 and z1 wires"

    try:
        dev2 = qp.device("default.qubit", wires = ["r0", "r1"])
        @qp.qnode(dev2)
        def circuit2():
            reece_operator()
            return qp.probs(dev2.wires)
        circuit2()
    except:
        assert False, "reece_operator can only act on r0 and r1 wires"
    try:
        dev3 = qp.device("default.qubit", wires = ["z1", "r1"])
        @qp.qnode(dev3)
        def circuit3():
            magic_operator()
            return qp.probs(dev3.wires)
        circuit3()
    except:
        assert False, "magic_operator can only act on r1 and z1 wires"


    for j in range(2):
        for k in range(2):
            assert np.isclose(circuit(j, k)[10 * j + 5 * k], 1), "The output is not correct"

# These are the public test cases
test_cases = [
    ('No input', 'No output')
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

#working in my red notebook, from quantum core.