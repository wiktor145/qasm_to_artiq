from openqasmparser import Qasm
from Interpreter import Interpreter


class NoQasmException(Exception):
    pass


class QASMFILEException(Exception):
    pass


class QasmToArtiqTranslator:

    def __init__(self, qasm_file=None, qasm_text=None):
        self.build_block_begin = '# <BUILD_BEGIN>'
        self.build_block_end = '# <BUILD_END>'

        self.run_block_begin = '# <RUN_BEGIN>'
        self.run_block_end = '# <RUN_END>'

        self.generated_functions_place = "# <GENERATED_FUNCTIONS>"

        self.output_file = './experiment.py'
        self.set_default_build_text()
        self.indent = "        "
        self.half_indent = "    "
        self.print_all_at_the_end = False
        self.experiment_name_to_change = "Skeleton for experiment"
        self.experiment_name = "Experiment 1"
        self.imports_place = "# <IMPORTS>"
        self.imports_list = []

        self.add_functions_generated_from_gates = True

        if qasm_file:
            f = open(qasm_file, "r")
            self.qasm_text = f.read()
            f.close()
        elif qasm_text:
            self.qasm_text = qasm_text
        else:
            raise NoQasmException("No source for QASM file or QASM text was given")

    def set_template_path(self, template_path):
        self.template_path = template_path

    def set_print_all_at_the_end(self, value):
        self.print_all_at_the_end = value

    def set_output_file(self, output_file):
        self.output_file = output_file

    def set_experiment_name(self, name):
        self.experiment_name = name

    def set_default_build_text(self):
        self.build_text = """self.setattr_device("core")"""

    def set_build_text_from_file(self, build_text_file):
        f = open(build_text_file, "r")
        self.set_build_text(f.read())
        f.close()

    def set_build_text(self, build_text):
        self.build_text = build_text

    def add_import(self, import_name):
        self.imports_list.append(import_name)

    def apply_imports(self, text):
        imports_text = ""
        for im in self.imports_list:
            imports_text += (im + "\n")

        text = text.replace(self.imports_place, imports_text)
        return text

    def load_template(self):
        try:
            f = open(self.template_path, "r")
            template_text = f.read()
            f.close()
            return template_text
        except FileNotFoundError as e:
            print("Template file {} was not found!".format(self.template_path))
            raise e

    def write_experiment_file(self, file_text):
        f = open(self.output_file, "w")
        f.write(file_text)
        f.close()

    def create_build_text(self):
        return self.build_text

    def create_run_and_functions_text(self, template_text):
        qasm = Qasm(data=self.qasm_text)
        ast = qasm.parse()
        print(ast.children)

        interpreter = Interpreter(text="", indent=self.indent, half_indent=self.half_indent, template_text=template_text,
                                  kernel_decorator="@kernel")
        ast.accept(interpreter)
        #print(ast.qasm())

        run_text = interpreter.text
        fun_text = interpreter.functions_text

        fun_text = fun_text.replace("lambda", "l")

        if self.print_all_at_the_end:
            run_text += self.indent + "self.print_all_cregs()\n"

        return run_text, fun_text

    def translate(self):
        template_text = self.load_template()
        # print(template_text)
        # print(template_text.split(self.build_block_begin))

        build_text = self.create_build_text()
        run_text, functions_text = self.create_run_and_functions_text(template_text)

        template_text = template_text.split(self.build_block_begin)[0] + build_text + \
                        template_text.split(self.build_block_end)[1]

        template_text = template_text.split(self.run_block_begin)[0] + run_text + \
                        template_text.split(self.run_block_end)[1]

        template_text = template_text.replace(self.experiment_name_to_change, self.experiment_name)
        template_text = self.apply_imports(template_text)

        if self.add_functions_generated_from_gates:
            template_text = template_text.replace(self.generated_functions_place, functions_text)

        self.write_experiment_file(template_text)


test = QasmToArtiqTranslator(qasm_file="./test.qasm")
test.set_template_path("./examples/no_hardware/repository/my_experiment2.py")
test.set_print_all_at_the_end(True)
test.set_experiment_name("Interpreter test")
test.add_import("import numpy as np")
test.add_import("from numpy import pi")
test.translate()

