# We define the Hamiltonian for you!
# represents sum: HCost = 3/4(ZiZj + Zi + Zj) - sum: -1(Zi)
# Z0Z1 = coeff 3/4, Z1Z2 = coeff 3/4, Z2Z0 = coeff 3/4, Z2Z3 = coeff 3/4
#Z0 = coeff 3/4 + 3/4  -1 = 1/2, Z1 = coeff 3/4 + 3/4 - 1 = 1/2, Z2 = coeff 3/4 + 3/4 + 3/4 - 1 = 5/4, Z3 = coeff 3/4 - 1 = -1/4
import json
import pennylane as qp
import pennylane.numpy as np
edges = [(0, 1), (1, 2), (2, 0), (2, 3)]
num_wires = 4

# We define the Hamiltonian for you!

ops = [qp.PauliZ(0), qp.PauliZ(1),qp.PauliZ(2), qp.PauliZ(3), qp.PauliZ(0)@qp.PauliZ(1), qp.PauliZ(0)@qp.PauliZ(2),qp.PauliZ(1)@qp.PauliZ(2),qp.PauliZ(2)@qp.PauliZ(3)]
coeffs = [0.5, 0.5, 1.25, -0.25, 0.75, 0.75, 0.75, 0.75]

cost_hamiltonian = qp.Hamiltonian(coeffs, ops)

# Write any helper functions you need here

def cost_hamiltonian_basic_gates(layer_param,noise_param):
    # sum: 3/4(ZiZj + Zi + Zj)
    for i,j in edges:

        #3/4ZiZj
        qp.CNOT(wires=[i,j])
        qp.DepolarizingChannel(noise_param, wires=j)
        # RZ is programmed as RZ(angle) = e^-i(angle/2)(Z), so times by two
        qp.RZ((3.0/4.0)*2.0*layer_param[0], j)
        qp.CNOT(wires=[i,j])
        qp.DepolarizingChannel(noise_param, wires=j)

        #3/4Zi + 3/4Zj
        qp.RZ((3.0/4.0)*2.0*layer_param[0], i)
        qp.RZ((3.0/4.0)*2.0*layer_param[0], j)
        
    # sum: -1(Zi)
    for i in range(num_wires):
        qp.RZ((-2.0)*layer_param[0], i)

def build_mixer_hamiltonian(layer_param):
    # sum: -1(Xi)
    for i in range(num_wires):
        qp.RX((2.0)*layer_param[1], i)
    
        
    


    

dev = qp.device('default.mixed', wires = num_wires)

@qp.qnode(dev) 
def qaoa_circuit(params, noise_param):

    """
    Define the noisy QAOA circuit with only CNOT and rotation gates, with Depolarizing noise
    in the target qubit of each CNOT gate.

    Args:
        params(list(list(float))): A list with length equal to the QAOA depth. Each element is a list that contains 
        the two QAOA parameters of each layer.
        noise_param (float): The noise parameter associated with the depolarization gate

    Returns: 
        (np.tensor): A numpy tensor of 1 element corresponding to the expectation value of the cost Hamiltonian
    
    """

    # Put your code here #
    for wire in range(num_wires):
        #state prep
        # qp.Hadamard(wires = wire)
        qp.RY(np.pi / 2.0, wires=wire)
    for layer_param in params:
        cost_hamiltonian_basic_gates(layer_param,noise_param)
        build_mixer_hamiltonian(layer_param)

    return qp.expval(cost_hamiltonian)

def approximation_ratio(qaoa_depth, noise_param):
    """
    Returns the approximation ratio of the QAOA algorithm for the Minimum Vertex Cover of the given graph
    with depolarizing gates after each native CNOT gate

    Args:
        qaoa_depth (float): The number of cost/mixer layer in the QAOA algorithm used
        noise_param (float): The noise parameter associated with the depolarization gate
    
    Returns: 
        (float): The approximation ratio for the noisy QAOA
    """

    # Put your code here #
    # with vertex 1 and vertex 2 as solution
    true_min_energy = -3.0 

    np.random.seed(2)
    init_params = np.array(
        np.random.uniform(-np.pi, np.pi, (qaoa_depth, 2)), requires_grad=True
    )
    # PennyLane optimizer
    opt = qp.GradientDescentOptimizer(stepsize=0.05)
    params = init_params

    #Run optimization loop for fixed number of steps
    # qaoa_depth is like number of layers in neural network, steps is number of epochs
    steps = 300
    for _ in range(steps):
        # updates the params of each layer to minimize the output of qaoa_circuit
        params = opt.step(lambda p: qaoa_circuit(p, noise_param), params)

    # eval with optimized layers
    min_expected_energy = qaoa_circuit(params, noise_param)

    # Calculate the approximation ratio as defined in the challenge:
    ratio = float(min_expected_energy / true_min_energy)

    return ratio



# These functions are responsible for testing the solution.
random_params = np.array([np.random.rand(2)])

ops_2 = [qp.PauliX(0), qp.PauliX(1), qp.PauliX(2), qp.PauliX(3)]
coeffs_2 = [1,1,1,1]

mixer_hamiltonian = qp.Hamiltonian(coeffs_2, ops_2)

@qp.qnode(dev)
def noiseless_qaoa(params):

    for wire in range(num_wires):

        qp.Hadamard(wires = wire)

    for elem in params:

        qp.ApproxTimeEvolution(cost_hamiltonian, elem[0], 1)
        qp.ApproxTimeEvolution(mixer_hamiltonian, elem[1],1)

    return qp.expval(cost_hamiltonian)

random_params = np.array([np.random.rand(2)])

circuit_check = (np.isclose(noiseless_qaoa(random_params) - qaoa_circuit(random_params,0),0))

def run(test_case_input: str) -> str:
    input = json.loads(test_case_input)
    output = approximation_ratio(*input)

    return str(output)

def check(solution_output: str, expected_output: str) -> None:
    solution_output = json.loads(solution_output)
    expected_output = json.loads(expected_output)
    
    names = list(qp.specs(qaoa_circuit)([[1,1]], 0.1)['resources'].gate_types.keys())
    random_params = np.array([np.random.rand(2)])

    assert circuit_check, "qaoa_circuit is not doing what it's expected to."

    assert names.count('ApproxTimeEvolution') == 0, "Your circuit must not use the built-in PennyLane Trotterization."
     
    assert set(names) == {'DepolarizingChannel', 'RX', 'RY', 'RZ', 'CNOT'}, "Your circuit must use qp.RX, qp.RY, qp.RZ, qp.CNOT, and qp.DepolarizingChannel."

    assert solution_output > expected_output - 0.02

# These are the public test cases
test_cases = [
    ('[2,0.005]', '0.4875'),
    ('[1, 0.003]', '0.1307')
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