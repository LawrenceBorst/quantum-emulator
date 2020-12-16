import circuit
import gates
import numpy as np

"""
Swaps all qubits, like a reflection. For instance |011> <-> |110>.
"""
def SWAP_all(n):
    def SWAP_adjacent(k, n):    # Swaps qubits k and k+1, k starting from 0 (!), n = # qubits
        result = np.identity(2 ** k)
        result = np.kron(result, gates.SWAP)
        result = np.kron(result, np.identity(2 ** (n - k - 2)))
        return result

    transform = np.identity(2 ** n)
    for i in range(n - 1):
        for j in range(n - i - 1):
            transform = np.matmul(transform, SWAP_adjacent(j, n))
    return transform

"""
The QFT. Returns the prototypical quantum fourier circuit
"""
def fourier(n, prepared=True, init_state = []):
    fourier_circuit = circuit.Circuit(n, prepared=prepared, init_state=init_state)

    if n == 1:
        fourier_circuit.append_layer("H")
        return fourier_circuit

    for i in range(n):
        # Layer with the H gate
        current_layer = []
        for j in range(i):
            current_layer.append("I")

        current_layer.append("H")

        for j in range(n - i - 1):
            current_layer.append("I")

        fourier_circuit.append_layer(*current_layer)

        # Layers with the rotations
        for j in range(1, n - i):
            fourier_circuit.append_layer(gates.CU(j+i, i, gates.R(2 * gates.PI / (2 ** (j + 1))), n))

    # Reflect the qubits (the QFT swaps their order by default)
    fourier_circuit.append_layer(SWAP_all(n))

    return fourier_circuit
