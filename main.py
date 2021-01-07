import algorithms
import gates
import numpy as np

circuit_qft = algorithms.qft(2)
circuit_iqft = algorithms.inverse_qft(2)

# Demonstrating that the correct matrix representation is obtained:
print("QFT matrix: ", circuit_qft.get_gate().round(decimals=3), "\n")
print("Inverse QFT matrix: ", circuit_iqft.get_gate().round(decimals=3), "\n")

# Running the qft circuit 10 times, resulting in 10 states from |0>...|3> each with equal probability
print("Output of Fourier transform on the computational basis: ", circuit_qft.execute(trials=10))

# Let's check the phase estimation algorithm using a T gate. We expect theta = 1/8 for u = |1> := [0, 1]
# Here theta = 1/8 corresponds in binary to 0.001, i.e. the first three qubits should read 001
circuit_phase = algorithms.phase_estimation(3, 1, gates.T, np.array([[0, 1]]))
print("Output of phase estimation on T with eigenvector [0,1], 3 decimal places: ", circuit_phase.execute(trials=10))

# As a quick check, this should output "00100" a bunch of times
circuit_phase = algorithms.phase_estimation(5, 1, gates.T, np.array([[0, 1]]))
print("Output of phase estimation on T with eigenvector [0,1], 5 decimal places: ", circuit_phase.execute(trials=10))

# Grover's algorithm
circuit_grover = algorithms.grover(3, 2)
print("Output of grover's algorithm with n=2, o=3: ", circuit_grover.execute(trials=10))
print("The explanation is that about 70% of the time 11 is chosen (reading the first two digits)\n",
      "which in essence means that the oracle is 11, i.e. 3.")