# # from qiskit.aqua import set_qiskit_aqua_logging
# import logging
# # from qiskit.aqua.components.feature_maps import SecondOrderExpansion
# # from qiskit.aqua.algorithms import QSVM
# # from qiskit.aqua import run_algorithm, QuantumInstance
# # from qiskit.aqua.input import ClassificationInput
# # from qiskit.aqua.utils import split_dataset_to_data_and_labels, map_label_to_class_name
# from qiskit import BasicAer
# # from datasets import *
# from qiskit import *
# # %matplotlib inline
# # Importing standard Qiskit libraries and configuring account
# # from qiskit import QuantumCircuit, execute, Aer, IBMQ
# # from qiskit.compiler import transpile, assemble
# # from qiskit.tools.jupyter import *
# # from qiskit.visualization import *

# # Loading your IBM Q account(s)
# # provider = IBMQ.load_account()

# q = QuantumRegister(2, 'q')
# c = ClassicalRegister(2, 'c')

# circuit = QuantumCircuit(q, c)

# ## Apply the quantum gates
# circuit.h(q[0])
# circuit.cx(q[0], q[1])

# ## Finish off with the measurements
# circuit.measure(q, c)

# ## Draw the circuit
# # %matplotlib inline

# # self.fig = plt.figure(figsize=(7, 7))
# circuit.draw(output="mpl")
# # plt.show()




# # setup aqua logging
# # qsvm = QSVM(feature_map, training_input, test_input, datapoints[0])


# make the imports that are necessary for our work
import qiskit as qk
from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit
from qiskit import execute, Aer
from qiskit import IBMQ
from qiskit.tools.visualization import plot_histogram
import matplotlib.pyplot as plt

# # simple function that applies a series of unitary gates from a given string
# def apply_secret_unitary(secret_unitary, qubit, quantum_circuit, dagger):
#     functionmap = {
#         'x': quantum_circuit.x,
#         'y': quantum_circuit.y,
#         'z': quantum_circuit.z,
#         'h': quantum_circuit.h,
#         't': quantum_circuit.t,
#     }
#     if dagger:
#         functionmap['t'] = quantum_circuit.tdg

#     if dagger:
#         [functionmap[unitary](qubit) for unitary in secret_unitary]
#     else:
#         [functionmap[unitary](qubit) for unitary in secret_unitary[::-1]]

# Create the quantum circuit
q = QuantumRegister(3)
c = ClassicalRegister(3)
qc = QuantumCircuit(q, c)

''' Qubit ordering as follows (classical registers will just contain measured values of the corresponding qubits):
q[0]: qubit to be teleported (Alice's first qubit. It was given to her after the application of a secret unitary 
    which she doesn't know)
q[1]: Alice's second qubit
q[2]: Bob's qubit, which will be the destination for the teleportation
'''
# simple function that applies a series of unitary gates from a given string

secret_unitary = 'hz'

def apply_secret_unitary(secret_unitary, qubit, quantum_circuit, dagger):
    functionmap = {
        'x': quantum_circuit.x,
        'y': quantum_circuit.y,
        'z': quantum_circuit.z,
        'h': quantum_circuit.h,
        't': quantum_circuit.t,
    }
    if dagger:
        functionmap['t'] = quantum_circuit.tdg

    if dagger:
        [functionmap[unitary](qubit) for unitary in secret_unitary]
    else:
        [functionmap[unitary](qubit) for unitary in secret_unitary[::-1]]

# Apply the secret unitary that we are using to generate the state to teleport. You can change it to any unitary
apply_secret_unitary(secret_unitary, q[0], qc, dagger=0)
qc.barrier()
# Next, generate the entangled pair between Alice and Bob (Remember: Hadamard followed by CX generates a Bell pair)
qc.h(q[1])
qc.cx(q[1], q[2])
qc.barrier()
# Next, apply the teleportation protocol.
qc.cx(q[0], q[1])
qc.h(q[0])
qc.measure(q[0], c[0])
qc.measure(q[1], c[1])
qc.cx(q[1], q[2])
qc.cz(q[0], q[2])
qc.barrier()

apply_secret_unitary(secret_unitary, q[2], qc, dagger=1)
qc.measure(q[2], c[2])

# fig = plt.figure()
qc.draw(output='mpl', filename="C:/temp/test-q.png")
# plt.show()

backend = Aer.get_backend('qasm_simulator')
job_sim = execute(qc, backend, shots=1024)
sim_result = job_sim.result()

measurement_result = sim_result.get_counts(qc)
print(measurement_result)
plot_histogram(measurement_result)


