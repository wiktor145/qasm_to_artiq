from artiq.experiment import *


# <IMPORTS>

class MyExperiment(EnvExperiment):
    """
    Skeleton for experiment
    """

    def build(self):
        # <BUILD_BEGIN>
        pass
        # <BUILD_END>

    def run(self):
        # <RUN_BEGIN>
        pass
        # <RUN_END>

    """Function generated from qasm"""

    # <GENERATED_FUNCTIONS>

    """Custom functions - should be implemented"""

    @kernel
    def U(self, theta, phi, l, q, q_nr):
        pass

    @kernel
    def CX(self, c, c_nr, t, t_nr):
        pass

    @kernel
    def prepare_cregs(self, name, no_of_regs):
        pass

    @kernel
    def prepare_qbits(self, name, no_of_qbits):
        pass

    @kernel
    def set_qbit(self, q, q_nr, val):
        pass

    # @kernel
    # def prepare_and_set_qbits(self, no_of_qbits, values):
    #     pass

    # @kernel
    # def measure_all(self):
    #     pass

    @kernel
    def print_all_qbits(self):
        pass

    @kernel
    def measure(self, qbit_name, qbit_nr, creg_name, creg_nr):
        pass

    # kernel?
    @kernel
    def conditional(self, creg, number):
        return True

    """User override implementations of basic gates"""

