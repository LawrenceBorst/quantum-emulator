import numpy as np
import gates
import state
import random

"""
Quantum circuit. Define:
self.circuit_symbolic:  an array that keeps track of the elements of the circuit,
                        e.g. [["I", "I"], ["H", "I"], ["CNT"]]. The first nesting
                        representings layers, the second the gates from top to bottom
                        "U" is reserved for any arbitrary transform (np array)
self.circuit:           The written out version of the above, where we do not use
                        strings but instead numpy matrices
init_state:             The initial state. Can be set to something like ("+", "-") (Bell states)
                        By default it is |0...0>, which represents input (0,...,0) (the associated array
                        in state.py is however [1, 0, 0..., 0]. This should not cause too much confusion)
"""

class Circuit:
    def __init__(self, n, prepared=False, init_state=[]):  # n = size of register
        self.n = n
        self.circuit = []
        self.circuit_symbolic = []
        self.init_state = state.State(n, prepared=prepared, state=init_state)

    def append_layer(self, *args):  # Gates could be, e.g. (n = 4)
        # (G) or (I, Z, I, Z)
        # Where G is custom-made and 16x16 numpy array
        layer = []
        layer_symbolic = []
        product = 1
        for (i, gate) in enumerate(args):
            if type(gate) != str:
                layer_symbolic.append("U")
            elif gate == "X":
                gate = gates.X
                layer_symbolic.append("X")
            elif gate == "Y":
                gate = gates.Y
                layer_symbolic.append("Y")
            elif gate == "Z":
                gate = gates.Z
                layer_symbolic.append("Z")
            elif gate == "H":
                gate = gates.H
                layer_symbolic.append("H")
            elif gate == "I":
                gate = gates.I
                layer_symbolic.append("I")
            elif gate == "CNOT":
                gate = gates.CNOT
                layer_symbolic.append("CNT")
                layer_symbolic.append("CNT")
            elif gate == "S":
                gate = gates.S
                layer_symbolic.append("S")
            else:
                layer_symbolic.append("U")

            row, col = gate.shape

            if row != col:
                raise Exception("A matrix is not square.")
            else:
                product *= row
                layer.append(gate)

        if product != 2 ** self.n:
            raise Exception("Dimensions of transform don't match that of register.")

        else:
            self.circuit.append(layer)
            self.circuit_symbolic.append(layer_symbolic)

    def get_circuit(self):
        return self.circuit

    def get_size(self):
        return self.n

    def measure(self):
        transforms = []

        # Here we make an array of matrices, one for each layer
        for layer in self.circuit:
            transform = np.array([1])
            for gate in layer:
                transform = np.kron(transform, gate)
            transforms.append(transform)

        # Here we simply apply the matrices
        output = self.init_state.get_state()
        for transform in transforms:
            output = np.matmul(transform, output)
        return output

    def get_gate(self):
        transforms = []

        # Here we make an array of matrices, one for each layer
        for layer in self.circuit:
            transform = np.array([1])
            for gate in layer:
                transform = np.kron(transform, gate)
            transforms.append(transform)

        result = np.identity(2 ** self.n)
        for transform in transforms:
            result = np.matmul(transform, result)

        return result

    def execute(self, trials = 1):
        probs = abs(self.measure()) ** 2
        basis = []

        # Create binary array
        for i in range(2**self.n):
            basis.append("{0:b}".format(i).zfill(self.n))   # Outputs array like [00, 01, 10, 11] (n = 2)

        return random.choices(basis, weights = probs, k = trials)

    def append_circuit(self, circ):
        if circ.get_size() != self.n:
            raise Exception("Cannot append circuits of different sizes")
        else:
            circ = circ.get_circuit()
            self.circuit.extend(circ)

    def draw(self):
        """Appends dashes to a string. E.g. X -> --X--, CTR -> -CTR-"""
        def append_dashes(str):
            return "-" * int((5 - len(str)) / 2) + str + "-" * int((5 - len(str)) / 2)

        output = ""
        for i in range(self.n):
            for j in range(len(self.circuit_symbolic)):
                output = output + append_dashes(self.circuit_symbolic[j][i])
            output += "\n"

        print(output)


        """
        --H----O---
               |
        --I----|---
               |
        --J----|---
               |
        -CNT---x---
        
        """
