import circuit
import gates
import numpy as np


"""
Swaps all qubits, like a reflection. For instance |011> <-> |110>.
In practice, we would just relabel the qubits
"""


def swap_all(n):
    def swap_adjacent(k, n):    # Swaps qubits k and k+1, k starting from 0 (!), n = qubits
        result = np.identity(2 ** k)
        result = np.kron(result, gates.SWAP)
        result = np.kron(result, np.identity(2 ** (n - k - 2)))
        return result

    transform = np.identity(2 ** n)
    for i in range(n - 1):
        for j in range(n - i - 1):
            transform = np.matmul(transform, swap_adjacent(j, n))
    return transform


"""
The QFT. Returns the prototypical quantum fourier circuit
"""


def qft(n, prepared=True, init_state=[]):
    qft_circuit = circuit.Circuit(n, prepared=prepared, init_state=init_state)

    if n == 1:
        qft_circuit.append_layer("H")
        return qft_circuit

    for i in range(n):
        # Layer with the H gate
        current_layer = []
        for j in range(i):
            current_layer.append("I")

        current_layer.append("H")

        for j in range(n - i - 1):
            current_layer.append("I")

        qft_circuit.append_layer(*current_layer)

        # Layers with the rotations
        for j in range(1, n - i):
            qft_circuit.append_layer(gates.CU(j+i, i, gates.R(2 * gates.PI / (2 ** (j + 1))), n))

    # Reflect the qubits (the QFT swaps their order by default)
    qft_circuit.append_layer(swap_all(n))

    return qft_circuit


"""
Essentially the QFt but with gates reversed. However, we can't simply revert the list of gates
because the rotation gates need their angle A sent to -A.
"""


def inverse_qft(n, prepared=True, init_state=[]):
    qft_circuit = circuit.Circuit(n, prepared=prepared, init_state=init_state)

    # Reflect the qubits (the QFT swaps their order by default)
    qft_circuit.append_layer(swap_all(n))

    if n == 1:
        qft_circuit.append_layer("H")
        return qft_circuit

    for i in range(n):
        i = n - i - 1
        # Layers with the rotations
        for j in range(1, n - i):
            qft_circuit.append_layer(gates.CU(j+i, i, gates.R((-1) * 2 * gates.PI / (2 ** (j + 1))), n))

        # Layer with the H gate
        current_layer = []
        for j in range(i):
            current_layer.append("I")

        current_layer.append("H")

        for j in range(n - i - 1):
            current_layer.append("I")

        qft_circuit.append_layer(*current_layer)

    return qft_circuit


"""
Quantum phase estimation
U = unitary numpy matrix
t = output of psi, i.e. the phase. Higher t -> higher precision. t ~ n + C with C between 1 and 4
n = number of qubits needed to store u, where u is an eigenvector of U. Clearly u = ln_2(N) where U is N by N
u = eigenvector, which can be found fast classically

We'll have to assume we know how to extract the eigenvector from U.
It turns out that an approximate eigenvector will also suffice at the cost of an commensurately approximate error
"""


def phase_estimation(t, n, U, u):
    # Get_power takes in U and returns U**(2**n)
    def U_2_n(U, n):
        for i in range(n):
            U = np.matmul(U, U)
        return U

    # Initialize the circuit
    init_state = []
    for i in range(t):
        init_state.append(0)
    init_state.append(u)

    phase_circuit = circuit.Circuit(n + t, init_state=init_state)

    # Apply hadamard gates to the first t qubits
    current_layer = []
    for i in range(t):
        current_layer.append("H")
    for i in range(n):
        current_layer.append("I")

    # Append first layer
    phase_circuit.append_layer(*current_layer)

    # Add the controlled U matrices
    for i in range(t):
        U2N = U_2_n(U, t - i - 1)
        U2N = gates.CU(i, t, U2N, n + t)
        phase_circuit.append_layer(U2N)

    # Add the inverse QFT gate
    IQFT = inverse_qft(t).get_gate()
    for i in range(n):
        IQFT = np.kron(IQFT, np.identity(2))
    phase_circuit.append_layer(IQFT)

    return phase_circuit


"""
Grover's search with 1 specific location.
n = number of qubits
o = oracle, encoded as an integer
finds a match in a list of 2^n elements
"""


def grover(o, n):
    # Create a CNOT controlled by all n qubits acting on the oracle qubit
    def make_CNOT_All():
        # Create a NOT gate controlled by all qubits
        Id = np.identity(2 ** (n + 1) - 2)
        X = gates.X
        # Direct sum of Id and X gives a CNOT gate controlled by all qubits acting on the last
        CNOT_All = np.zeros(np.add(Id.shape, X.shape))
        CNOT_All[:Id.shape[0],:Id.shape[1]] = Id
        CNOT_All[Id.shape[0], Id.shape[1]:] = X
        return CNOT_All

    """
    Create the oracle circuit. We create a first layer of X and I gates
    Then a layer of 
    Then repeat the first layer
    The overall result is three layers, acting as a controlled NOT gate that flips the final qubit if
    and only if the first n qubits correspond to the sought-after index
    I.e. |x>|q> -> |x>|(f(x) + q) (mod 2)>
    """
    def make_oracle_circuit():
        oracle_circuit = circuit.Circuit(n + 1, prepared=True)
        first_third_layer = []


        second_layer = [make_CNOT_All()]
        oracle_circuit.append_layer(*second_layer)

        oracle_circuit.append_layer(first_third_layer)

    # Oracle matrix transformation
    oracle = np.identity(2 ** n)
    oracle[o, o] = - 1

    init_state = []
    for i in range(n):
        init_state.append(0)
    init_state.append(1)
    grover_circuit = circuit.Circuit(n + 1, init_state=init_state)

    # First layer with the Hadamard gates
    current_layer = []
    for i in range(n+1):
        current_layer.append("H")
    grover_circuit.append_layer(*current_layer)
