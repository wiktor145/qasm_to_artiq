from artiq.experiment import *


import numpy as np
from numpy import pi



class MyExperiment(EnvExperiment):
    """
    Interpreter test
    """

    def build(self):
        self.setattr_device("core")

    def run(self):
        self.prepare_qbits('q', 3)
        self.prepare_cregs('c', 3)
        self.h('q', 1)
        with parallel:
            self.h('q', 0)
            self.h('q', 1)
            self.h('q', 2)
        with parallel:
            self.x('q', 0)
            self.x('q', 1)
            self.x('q', 2)
        self.x('q', 2)
        self.set_qbit('q', 0, 0)
        self.ccx('q', 0, 'q', 1, 'q', 2)
        if self.conditional('c', 3):
            self.x('q', 2)
        self.cx('q', 1, 'q', 2)
        self.measure('q', 0, 'c', 0)
        self.measure('q', 1, 'c', 1)
        self.measure('q', 2, 'c', 2)
        self.print_all_cregs()


    """Function generated from qasm"""

    

    @kernel
    def u3(self, theta, phi, l, q, q_nr):
        self.U(theta, phi, l, q, q_nr)

    @kernel
    def u2(self, phi, l, q, q_nr):
        self.U((pi/2), phi, l, q, q_nr)

    @kernel
    def u1(self, l, q, q_nr):
        self.U(0, 0, l, q, q_nr)

    @kernel
    def id(self, a, a_nr):
        self.U(0, 0, 0, a, a_nr)

    @kernel
    def u0(self, gamma, q, q_nr):
        self.U(0, 0, 0, q, q_nr)

    @kernel
    def y(self, a, a_nr):
        self.u3(pi,(pi/2),(pi/2), a, a_nr)


    @kernel
    def z(self, a, a_nr):
        self.u1(pi, a, a_nr)


    @kernel
    def s(self, a, a_nr):
        self.u1((pi/2), a, a_nr)


    @kernel
    def sdg(self, a, a_nr):
        self.u1((-(pi)/2), a, a_nr)


    @kernel
    def t(self, a, a_nr):
        self.u1((pi/4), a, a_nr)


    @kernel
    def tdg(self, a, a_nr):
        self.u1((-(pi)/4), a, a_nr)


    @kernel
    def rx(self, theta, a, a_nr):
        self.u3(theta,(-(pi)/2),(pi/2), a, a_nr)


    @kernel
    def ry(self, theta, a, a_nr):
        self.u3(theta,0,0, a, a_nr)


    @kernel
    def rz(self, phi, a, a_nr):
        self.u1(phi, a, a_nr)


    @kernel
    def cz(self, a, a_nr, b, b_nr):
        self.h(b, b_nr)
        self.cx(a, a_nr, b, b_nr)
        self.h(b, b_nr)


    @kernel
    def cy(self, a, a_nr, b, b_nr):
        self.sdg(b, b_nr)
        self.cx(a, a_nr, b, b_nr)
        self.s(b, b_nr)


    @kernel
    def swap(self, a, a_nr, b, b_nr):
        self.cx(a, a_nr, b, b_nr)
        self.cx(b, b_nr, a, a_nr)
        self.cx(a, a_nr, b, b_nr)


    @kernel
    def ch(self, a, a_nr, b, b_nr):
        self.h(b, b_nr)
        self.sdg(b, b_nr)
        self.cx(a, a_nr, b, b_nr)
        self.h(b, b_nr)
        self.t(b, b_nr)
        self.cx(a, a_nr, b, b_nr)
        self.t(b, b_nr)
        self.h(b, b_nr)
        self.s(b, b_nr)
        self.x(b, b_nr)
        self.s(a, a_nr)


    @kernel
    def cswap(self, a, a_nr, b, b_nr, c, c_nr):
        self.cx(c, c_nr, b, b_nr)
        self.ccx(a, a_nr, b, b_nr, c, c_nr)
        self.cx(c, c_nr, b, b_nr)


    @kernel
    def crz(self, l, a, a_nr, b, b_nr):
        self.u1((l/2), b, b_nr)
        self.cx(a, a_nr, b, b_nr)
        self.u1((-(l)/2), b, b_nr)
        self.cx(a, a_nr, b, b_nr)


    @kernel
    def cu1(self, l, a, a_nr, b, b_nr):
        self.u1((l/2), a, a_nr)
        self.cx(a, a_nr, b, b_nr)
        self.u1((-(l)/2), b, b_nr)
        self.cx(a, a_nr, b, b_nr)
        self.u1((l/2), b, b_nr)


    @kernel
    def cu3(self, theta, phi, l, c, c_nr, t, t_nr):
        self.u1(((l-phi)/2), t, t_nr)
        self.cx(c, c_nr, t, t_nr)
        self.u3((-(theta)/2),0,(-((phi+l))/2), t, t_nr)
        self.cx(c, c_nr, t, t_nr)
        self.u3((theta/2),phi,0, t, t_nr)


    @kernel
    def rzz(self, theta, a, a_nr, b, b_nr):
        self.cx(a, a_nr, b, b_nr)
        self.u1(theta, b, b_nr)
        self.cx(a, a_nr, b, b_nr)


    """Custom functions - should be implemented"""

    @kernel
    def U(self, theta, phi, l, q, q_nr):
        print("Applying U gate to {} {} {} {} {}".format(theta, phi, l, q, q_nr))

    @kernel
    def CX(self, c, c_nr, t, t_nr):
        print("Applying CX to {} {} {} {}".format(c, c_nr, t, t_nr))

    @kernel
    def prepare_cregs(self, name, no_of_regs):
        print("Preparing creg {} with size {}".format(name, no_of_regs))

    @kernel
    def prepare_qbits(self, name, no_of_qbits):
        print("Preparing qbits {} with size {}".format(name, no_of_qbits))

    @kernel
    def set_qbit(self, q, q_nr, val):
        print("Setting qbit {} {} to {}".format(q, q_nr, val))

    # @kernel
    # def prepare_and_set_qbits(self, no_of_qbits, values=[]):
    #     self.prepare_qbits(no_of_qbits)
    #     if values == []:
    #         for i in range(no_of_qbits):
    #             self.set_qbit(i, np.array([1, 0]))
    #     else:
    #         for i, val in enumerate(values):
    #             self.set_qbit(i, val)

    @kernel
    def measure_all(self):
        pass

    @kernel
    def measure(self, qbit_name, qbit_nr, creg_name, creg_nr):
        print("Measuring qbit {} {} to creg {} {}".format(qbit_name, qbit_nr, creg_name, creg_nr))

    @kernel
    def print_all_cregs(self):
        print("Printing all cregs...")

    """User override implementations of basic gates"""

    @kernel
    def x(self, qbit_nr):
        print("Applying X gate to qbit {}".format(qbit_nr))
        self.qbits[qbit_nr] = np.array([[0, 1], [1, 0]]) @ self.qbits[qbit_nr]

    @kernel
    def cx(self, control, target):
        print("Applying control not gate from {} to {}".format(control, target))

    @kernel
    def ccx(self, control1, control2, target):
        print("Applying ccx gate from {} and {} to {}".format(control1, control2, target))

    @kernel
    def h(self, qbit_nr):
        print("Applying hadamard gate to {}".format(qbit_nr))

    # kernel?
    @kernel
    def conditional(self, creg, number):
        print("Checking whether creg {} is equal to {}".format(creg, number))
        return True
