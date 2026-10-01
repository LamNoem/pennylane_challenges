import json
import pennylane as qp
import pennylane.numpy as np
np.random.seed(1967)

def get_matrix(params):
    """
    Args:
        - params (array): The four parameters of the model.
        
    Returns:
        - (matrix): The associated matrix to these parameters.
    """

    alpha, beta, gamma, phi = params

    #  Rz(alpha) using np.stack 
    r1_alpha = np.stack([np.exp(-1j * alpha / 2), 0.0 + 0j])
    r2_alpha = np.stack([0.0 + 0j, np.exp(1j * alpha / 2)])
    rz_alpha = np.stack([r1_alpha, r2_alpha])

    #  Rx(beta)
    r1_beta = np.stack([np.cos(beta / 2), -1j * np.sin(beta / 2)])
    r2_beta = np.stack([-1j * np.sin(beta / 2), np.cos(beta / 2)])
    rx_beta = np.stack([r1_beta, r2_beta])

    #  Rz(gamma)
    r1_gamma = np.stack([np.exp(-1j * gamma / 2), 0.0 + 0j])
    r2_gamma = np.stack([0.0 + 0j, np.exp(1j * gamma / 2)])
    rz_gamma = np.stack([r1_gamma, r2_gamma])

    
    global_phase = np.exp(1j * phi)
    matrix = global_phase * (rz_gamma @ rx_beta @ rz_alpha)

    return matrix

    # Return the matrix

def error(U, params):
    """
    This function determines the similarity between your generated matrix and
    the target unitary.

    Args:
        - U (np.array): Goal matrix that we want to approach.
        - params (array): The four parameters of the model.

    Returns:
        - (float): Error associated with the quality of the solution.
    """

    matrix = get_matrix(params)

    # Put your code here #

    # Return the error
    matrix_difference = U - matrix
    loss = np.sqrt(np.sum(np.abs(matrix_difference) ** 2))
    return loss

def train_parameters(U):
    epochs = 1000
    lr = 0.01

    grad = qp.grad(error, argnums=1)
    params = np.random.rand(4) * np.pi

    for epoch in range(epochs):
        params -= lr * grad(U, params)

    return params

# These functions are responsible for testing the solution.
def run(test_case_input: str) -> str:
    matrix = json.loads(test_case_input)
    params = [float(p) for p in train_parameters(matrix)]
    return json.dumps(params)


def check(solution_output: str, expected_output: str) -> None:
    matrix1 = get_matrix(json.loads(solution_output))
    matrix2 = json.loads(expected_output)
    assert not np.allclose(get_matrix(np.random.rand(4)), get_matrix(np.random.rand(4)))
    assert np.allclose(matrix1, matrix2, atol=0.2)