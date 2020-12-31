import numpy as np
import random
import math

"""
The qubit is represented by an array [a, b]
representing a|0> + b|1>. We use the canonical
representation (Bloch sphere) to initiate a and b
"""


class Qubit:
    def __init__(self, prepared=False):
        if not prepared:
            phi = random.random() * 2 * math.pi
            theta = random.random() / 2 * math.pi
            rel_phase = np.cos(phi) + np.sin(phi) * 1j
            self.qubit = np.array([[np.cos(theta), np.sin(theta) * rel_phase]]).T
        else:
            self.qubit = np.array([[1, 0]], dtype=complex).T

    def get_qubit(self):
        return self.qubit
