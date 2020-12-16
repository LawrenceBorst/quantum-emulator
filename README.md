# quantum-emulator
Rudimentary quantum emulator in Python
This is a simple quantum emulator, but not quite to the extent of using the register formality, as some quantum programming languages do. See it more like a quantum playground.

I'm in the process of implementing several well-known quantum algorithms, and so far all the logic is set up to create circuits from gates and states (where states are made from qubits). Algorithms are then implemented as circuits.

For instance, main.py has the code <code>circuit = algorithms.fourier(3)</code>. Very simple, but under the hood we have made the whole QFT circuit for 3 qubits with the register initialized as |000>. We can grab the QFT matrix (the standard FT matrix for 8 bits) with <code>circuit.get_gate()</code>. This function simply returns the complete circuit as if it were a single matrix/gate.

Likewise, we can just execute the circuit like we would in a real quantum computer, producing classical bits by observing the output. For 5 "trials", write <code>circuit.execute(trials = 5)</code>. For this circuit, you'll get 5 states out of a possible 8 from a uniform distribution.
