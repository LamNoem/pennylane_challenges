





#notes
# The qp.DepolarizingChannel is a quantum noise operation in PennyLane that models a uniform loss of information across a qubit system. It simulates a scenario where a qubit has a specific probability of either remaining completely unaffected or being replaced by a completely random, uninformative state (known as the maximally mixed state).

# When you apply a depolarizing channel to a single qubit density matrix ρ, the mathematical transformation is:
# \(\mathcal{E}(\rho )=(1-p)\rho +p\frac{I}{2}\)


# When applied to a single-qubit density matrix \(\rho \), the PennyLane Depolarizing Channel transforms each element of the matrix uniformly.
# Let the initial density matrix be written out by its individual elements:
# \(\rho =\left(\begin{matrix}\rho _{00}&\rho _{01}\\ \rho _{10}&\rho _{11}\end{matrix}\right)\)
# Where:
# • \(\rho _{00}\) is the population of the ground state \(\vert{}0\rangle\).
# • \(\rho _{11}\) is the population of the excited state \(\vert{}1\rangle\).
# • \(\rho _{01}\) and \(\rho _{10}\) are the complex coherences (the quantum superpositions).
# Applying the depolarizing channel with an error probability parameter \(p\) modifies the elements as follows:
# 1. The Diagonal Elements (Populations)
# The populations are mixed with the identity matrix contribution (\(0.5\)). The new diagonal elements become:
# \(\rho _{00}^{\text{new}}=(1-p)\rho _{00}+\frac{p}{2}\)
# \(\rho _{11}^{\text{new}}=(1-p)\rho _{11}+\frac{p}{2}\)
# • What happens: The original population shrinks by a factor of \((1-p)\), while a flat background noise of \(\frac{p}{2}\) is added to both states.
# • If \(p = 1\) (maximum depolarization), both \(\rho _{00}\) and \(\rho _{11}\) force-collapse to exactly \(0.5\), meaning the qubit has a 50/50 chance of being in either state regardless of where it started.
# 2. The Off-Diagonal Elements (Coherences)
# The off-diagonal elements do not receive any additive noise term because the identity matrix has zeroes on its off-diagonals. They simply decay:
# \(\rho _{01}^{\text{new}}=(1-p)\rho _{01}\)
# \(\rho _{10}^{\text{new}}=(1-p)\rho _{10}\)
# • What happens: The quantum coherence decays directly by a factor of \((1-p)\).
# • If \(p = 1\), the off-diagonals become exactly \(0\), meaning all phase information and quantum superposition characteristics are completely wiped out.
# The Transformed Matrix Summary
# Putting it all together, the final state looks like this:
# \(\rho ^{\text{new}}=\left(\begin{matrix}(1-p)\rho _{00}+\frac{p}{2}&(1-p)\rho _{01}\\ (1-p)\rho _{10}&(1-p)\rho _{11}+\frac{p}{2}\end{matrix}\right)\)



#Expand the density matrix into separate qubit slots
# Let's look at the Pauli word component \(P = P_1 \otimes P_2 \otimes \dots \otimes P_n\). The noise operator acts on each slot individually:
# \(\Delta _{\lambda }^{\otimes n}[P]=\left(\Delta _{\lambda }[P_{1}]\right)\otimes \left(\Delta _{\lambda }[P_{2}]\right)\otimes \dots \otimes \left(\Delta _{\lambda }[P_{n}]\right)\)