import logging
import numpy as np
from artiq.experiment import *


class TestExperiment(EnvExperiment):
    """
    Test experiment
    """

    def build(self):
        self.setattr_device("core")

    # """This function will be autmoatically filled"""
    #
    # def run(self):
    #     """<RUN_BEGIN>"""
    #     pass
    #     """<RUN_END>"""

    @kernel
    def run(self):
        self.prepare_and_set_qbits(2)
        self.prepare_cregs(2)
        self.x(1)
        self.measure(0, 0)
        self.measure(1, 1)
        self.print_all_qbits()

    """These are functions that will be executed in /run/ after translation from QASM"""

    @kernel
    def prepare_cregs(self, no_of_regs):
        self.cregs = [-1 for _ in range(no_of_regs)]

    @kernel
    def prepare_qbits(self, no_of_qbits):
        print("Preparing {} qbits...".format(no_of_qbits))
        self.qbits = [-1 for _ in range(no_of_qbits)]

    @kernel
    def set_qbit(self, qbit_nr, value):
        print("Setting qbit {} to value {}".format(qbit_nr, value))
        self.qbits[qbit_nr] = value

    @kernel
    def prepare_and_set_qbits(self, no_of_qbits, values=[]):
        self.prepare_qbits(no_of_qbits)
        if values == []:
            for i in range(no_of_qbits):
                self.set_qbit(i, np.array([1, 0]))
        else:
            for i, val in enumerate(values):
                self.set_qbit(i, val)

    @kernel
    def x(self, qbit_nr):
        print("Applying X gate to qbit {}".format(qbit_nr))
        self.qbits[qbit_nr] = np.array([[0, 1], [1, 0]]) @ self.qbits[qbit_nr]

    @kernel
    def measure_all(self):
        pass

    @kernel
    def measure(self, qbit_nr, creg_nr):
        print("Measuring qbit {}".format(qbit_nr))
        self.cregs[creg_nr] = 0 if self.qbits[qbit_nr][0] == 1 and self.qbits[qbit_nr][1] == 0 else 1

    @kernel
    def print_all_qbits(self):
        for i, a in enumerate(self.cregs):
            print("Register {} value {}".format(i, a))

    @kernel
    def cx(self, control, target):
        print("Applying control not gate from {} to {}".format(control, target))

    @kernel
    def ccx(self, control1, control2, target):
        print("Applying ccx gate from {} and {} to {}".format(control1, control2, target))

    @kernel
    def h(self, qbit_nr):
        print("Applying hadamard gate to {}".format(qbit_nr))
