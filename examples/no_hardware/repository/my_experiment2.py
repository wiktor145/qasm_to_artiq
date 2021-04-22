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
