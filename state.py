import qubit
import numpy as np

"""
For simplicity, state will be defined as an array
of complex numbers whose inner product equals 1.
In truth, it comes from a selection of qubits
One state could be:
|psi> = a|00> + b|01> + c|10> + d|11>
Represented by [a, b, c, d] e.g. |c|**2 represents the
probability that |psi> will collapse |10>
"""


class State:
    def __init__(self, n, prepared=True, state=[]):
        if state:  # If a state is custom
            if len(state) != n:
                raise Exception("State must be the same length as the number of qubits.")
            final_state = np.array([1])
            for vec in state:
                if vec == 0:
                    final_state = np.kron(final_state, np.array([[1, 0]], dtype=complex).T)
                elif vec == 1:
                    final_state = np.kron(final_state, np.array([[0, 1]], dtype=complex).T)
                elif vec == '+':
                    final_state = np.kron(final_state, 1 / np.sqrt(2) * np.array([[1, 1]], dtype=complex).T)
                elif vec == '-':
                    final_state = np.kron(final_state, 1 / np.sqrt(2) * np.array([[1, -1]], dtype=complex).T)
            state = final_state

        elif prepared == True:  # Prepared state [1, 0,...,0]
            state = qubit.Qubit(prepared=True).get_qubit()
            for i in range(n - 1):
                state = np.kron(state, qubit.Qubit(prepared=True).get_qubit())

        else:  # Random state (array of random complex probabilities)
            state = qubit.Qubit().get_qubit()
            for i in range(n - 1):
                state = np.kron(state, qubit.Qubit().get_qubit())
        self.state = state

    def get_state(self):
        return self.state

    def set_state(self, np_arr):
        self.state = np_arr
