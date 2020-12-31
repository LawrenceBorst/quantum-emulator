import algorithms
import gates
import numpy as np

circuit_qft = algorithms.qft(2)
circuit_iqft = algorithms.inverse_qft(2)

# Demonstrating that the correct matrix representation is obtained:
print(circuit_qft.get_gate(), "\n")
print(circuit_iqft.get_gate(), "\n")

# Running the qft circuit 10 times, resulting in 10 states from |0>...|3> each with equal probability
print(circuit_qft.execute(trials = 10))

# Let's check the phase estimation algorithm using a T gate. We expect theta = 1/8 for u = |1> := [0, 1]
# Here theta = 1/8 corresponds in binary to 0.001, i.e. the first three qubits should read 001
circuit_phase = algorithms.phase_estimation(3, 1, gates.T, np.array([[0, 1]]))
print(circuit_phase.execute(trials=10))

