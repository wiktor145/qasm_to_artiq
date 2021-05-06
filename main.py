from openqasmparser import Qasm
from Interpreter import Interpreter
from translator import QasmToArtiqTranslator

test = QasmToArtiqTranslator(qasm_file="./test.qasm")
test.set_template_path("./examples/no_hardware/repository/my_experiment2.py")
test.set_print_all_at_the_end(True)
test.set_experiment_name("Interpreter test")
test.add_import("import numpy as np")
test.add_import("from numpy import pi")
test.translate()

