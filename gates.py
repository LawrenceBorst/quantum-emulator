import numpy as np

"""
The quantum gates, represented by matrices.
"""

PI = 3.1415926535897932384626433

X = np.array([[0, 1],
              [1, 0]], dtype=complex)  # Pauli X
Y = np.array([[0, -1j],
              [1j, 0]], dtype=complex) # Pauli Y
Z = np.array([[1, 0],
              [0, -1]], dtype=complex) # Pauli Z

S = np.array([[1, 0],
              [0, 1j]], dtype=complex) # Phase

T = np.array([[1, 0],
             [0, np.exp(1j*PI/4)]], dtype=complex)     # T (pi / 8)

H = 1 / np.sqrt(2) * np.array([[1, 1],
                               [1, -1]], dtype=complex)     # Hadamard

I = np.array([[1, 0],
              [0, 1]], dtype=complex) # Identity

CNOT = np.array([[1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 0, 1],
                [0, 0, 1, 0]], dtype=complex)

SWAP = np.array([[1, 0, 0, 0],
                 [0, 0, 1, 0],
                 [0, 1, 0, 0],
                 [0, 0, 0, 1]])

def R(phi):
    return np.array([[1, 0],
                     [0, np.exp(1j*phi)]], dtype=complex)   # Common matrix performing rotation around z-axis

"""
Controlled Unitary Operator.    ctrl=control qubit (1 to n)
                                targ = target qubit (1 to n)
                                U = 2 by 2 unitary matrix
                                n = number of qubits
"""
def CU(ctrl, targ, U, n):
    if ctrl < targ:
        output = np.kron(U-np.identity(2), np.identity(2 ** (n - targ - 1)))
        output = np.kron(np.identity(2 ** (targ-1-ctrl)), output)
        output = np.kron(np.identity(2) - Z, output)
        output = 1 / 2 * np.kron(np.identity(2 ** ctrl), output)
        output = output + np.identity(2 ** n)
    else:
        output = np.kron(np.identity(2)-Z, np.identity(2 ** (n - ctrl - 1)))
        output = np.kron(np.identity(2 ** (ctrl - 1 - targ)), output)
        output = np.kron(U - np.identity(2), output)
        output = 1 / 2 * np.kron(np.identity(2 ** targ), output)
        output = output + np.identity(2 ** n)
    return output
