import json
import pennylane as qp
import pennylane.numpy as np
def W(params):
    
    """
    Subcircuit that implements the trainable block W
    
    Args:
        params (np.array): A matrix containing the parameters for the trainable block W. The length of
        params is equal to the depth of the circuit. The length of each row in params is the number 
        of qubits used. See the challenge statement for a detailed explanation
    Returns:
        Since this function is a subcircuit, you must not return anything.
    
    """
    

    # Put your code here
    for layer in params:
        for i,param in enumerate(layer):
            qp.RY(param,wires=i)

        for i in range(len(layer)-1):
            qp.CNOT(wires=[i,i+1])

        qp.CNOT(wires=[len(layer)-1, 0])

def S(g, x, num_wires):
    
    """
    Subcircuit that implements the encoding block S
    
    Args:
        g (pennylane.Operator): A PennyLane operator representing the generator for the encoding
        gates. It must be Hermitian in order to generate a unitary. Call it as g(wires) to specify
        the wires on which it acts.
        x (complex): The scalar coefficient of the operator g.
        num_wires (int): The number of wires over which the encoding gate is broadcast.
        
        
    Returns:
        Since this function is a subcircuit, you must not return anything.
    
    """
    

    # Put your code here
    for i in range(num_wires):
        qp.evolve(g(wires=i), coeff=-x)
    

# Create a device

dev = qp.device("default.qubit")

@qp.qnode(dev)
def quantum_model(param_set, g, x):
    
    """
    This QNode implements the quantum model with alternating trainable and encoding blocks
    
    Args:
        param_set (np.array): A numpy array whose elements are the parameter matrices for each of the trainable
        blocks. Therefore, the length of this list is equal to the number of trainable blocks, which is greater
        than, or equal to 2.
        g (pennylane.Operator): A PennyLane operator representing the generator for the encoding
        gates. It must be Hermitian in order to generate a unitary.
        x: The scalar coefficient of the operator g.
    Returns:
        (np.tensor(float)): A tensor of dimensions (2,) representing the measurement probabilities in the computational 
        basis on the first wire.
    """
    

    # Put your code here
    num_wires = len(param_set[0][0])  

    for i, matrix in enumerate(param_set): 
        W(matrix)

        if i < len(param_set) - 1:  
            S(g, x, num_wires)

    return qp.probs(wires=0)
    

# These functions are used to test your solution

def run(test_case_input: str) -> str:
    ins = json.loads(test_case_input)
    params = np.array(ins[0])
    g = getattr(qp, ins[1])
    x = ins[2]
    outs = quantum_model(params, g, x).tolist()
    return str(outs)

def check(solution_output: str, expected_output: str) -> None:
    solution_output = json.loads(solution_output)
    expected_output = json.loads(expected_output)
    
    dev_test = qp.device("default.qubit", wires = [0,1,2])    
    
    @qp.qnode(dev_test)
    def w_node(params):
        
        W(params)
        
        return qp.probs(wires = [0,1]) 
    
    @qp.qnode(dev_test)
    def s_node(g, x, num_wires):
        
        S(g, x, num_wires)
        
        return qp.probs(wires = [0,1]) 
        
    params_test = np.array([[np.pi, np.pi/4, np.pi],[np.pi, np.pi/4, np.pi/3]])
    w_test = w_node(params_test)
    
    s_test = s_node(qp.PauliX, np.pi/7, 3)
    
    assert np.allclose(w_test, [0.10983496, 0.21338835, 0.03661165, 0.64016504], atol = 1e-3), "Something isn't quite right with the trainable block."
    
    assert np.allclose(s_test, [0.65892978, 0.15281512, 0.15281512, 0.03543998], atol = 1e-3), "Something isn't quite right with the encoding block."
    
    assert np.allclose(solution_output,expected_output, atol = 1e-3), "Not the correct probabilities for the quantum model."