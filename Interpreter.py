from visit import *
import sys
import numpy as np

import openqasmparser.node
from openqasmparser.node import *

sys.setrecursionlimit(10000)


# todo external
# todo opaque, które nic nie robi
# todo w bramkach i w measure ogarniać zarówno indexedid (q[1]) jak i id (q) ????

class Interpreter(object):
    def __init__(self, template_text, text, indent, half_indent, kernel_decorator, parallel_on_wrg):
        self.text = text
        self.template_text = template_text
        self.indent = indent
        self.functions_text = ""
        self.half_indent = half_indent
        self.do_not_override_user_defined = True
        self.kernel_decorator = kernel_decorator
        self.parallel_on_whole_register_gates = parallel_on_wrg
        self.registers_sizes = {}

    @on('node')
    def visit(self, node):
        print(type(node))
        pass

    def get_arguments_list_from_children_id_list(self, children):
        ret = ""
        for a in children:
            if ret:
                ret += ", "
            ret += str(a.name) + ", " + str(a.name) + "_nr"
        return ret

    def get_arguments_from_universal_unitary(self, c):
        text = ""
        # print(c.children[0])
        # print(c.children[1])

        for e in c.children[0].children:
            # print(e.qasm())
            text += e.qasm() + ", "

        text += c.children[1].name + ", " + c.children[1].name + "_nr"
        return text

    def get_gate_body(self, body, bitlist):
        body_text = ""

        for c in body.children:
            if isinstance(c, openqasmparser.node.universalunitary.UniversalUnitary):
                body_text += self.indent + "self.U({})".format(self.get_arguments_from_universal_unitary(c))
            elif isinstance(c, openqasmparser.node.cnot.Cnot):
                body_text += self.indent + "self.CX({}, {}, {}, {})".format(c.children[0].name,
                                                                            c.children[0].name + "_nr",
                                                                            c.children[1].name,
                                                                            c.children[1].name + "_nr")
            elif isinstance(c, openqasmparser.node.customunitary.CustomUnitary):
                body_text += self.indent + "self." + c.name + "({}{})\n".format(
                    c.arguments.qasm() + ", " if c.arguments is not None else "",
                    self.get_arguments_list_from_children_id_list(c.bitlist.children))
        # print(body_text)
        return body_text

    @when(openqasmparser.node.gate.Gate)
    def visit(self, node):
        gate_function_name = node.name
        arguments_list = "(self, "
        if node.arguments:
            for arg in node.arguments.children:
                arguments_list += arg.name + ", "

        if node.bitlist:
            for arg in node.bitlist.children:
                arguments_list += arg.name + ", " + arg.name + "_nr, "
        arguments_list = arguments_list[:-2] + ")"

        gate_body = self.get_gate_body(node.body, node.bitlist)

        fun_begin = "def " + gate_function_name + "("

        if self.do_not_override_user_defined:
            if fun_begin not in self.template_text:
                self.functions_text += "\n\n" + self.half_indent + self.kernel_decorator + "\n" + self.half_indent \
                                       + "def " + gate_function_name + arguments_list + ":\n"
                self.functions_text += gate_body

    @when(openqasmparser.node.program.Program)
    def visit(self, node):
        if isinstance(node.children, list):
            for elem in node.children:
                elem.accept(self)
        else:
            node.children.accept(self)

    @when(openqasmparser.node.qreg.Qreg)
    def visit(self, node):
        base = "self.prepare_qbits('{}', {})\n".format(node.name, node.index)
        self.add_text_with_indent(base)
        self.registers_sizes[node.name] = node.index

    @when(openqasmparser.node.creg.Creg)
    def visit(self, node):
        base = "self.prepare_cregs('{}', {})\n".format(node.name, node.index)
        self.add_text_with_indent(base)
        self.registers_sizes[node.name] = node.index

    def get_arguments_list_from_children_index_list(self, children):
        ret = ""
        for a in children:
            if ret:
                ret += ", "
            ret += "'" + a.name + "'" + ", " + str(a.index)
        return ret

    @when(openqasmparser.node.customunitary.CustomUnitary)
    def visit(self, node):
        base = ""
        if isinstance(node.bitlist.children[0], openqasmparser.node.indexedid.IndexedId):
            base = "self." + node.name + "({})\n".format(
                self.get_arguments_list_from_children_index_list(node.bitlist.children))
        else:  # Id
            if self.parallel_on_whole_register_gates:
                base += "with parallel:\n"
                for i in range(self.registers_sizes[node.bitlist.children[0].name]):
                    base += self.half_indent + self.indent + "self." + node.name + "('{}', {})\n".format(
                        node.bitlist.children[0].name, i)

            else:
                for i in range(self.registers_sizes[node.bitlist.children[0].name]):
                    if i:
                        base += self.indent + "self." + node.name + "('{}', {})\n".format(node.bitlist.children[0].name,
                                                                                          i)
                    else:
                        base += "self." + node.name + "('{}', {})\n".format(node.bitlist.children[0].name, i)

        self.add_text_with_indent(base)

    @when(openqasmparser.node.measure.Measure)
    def visit(self, node):
        base = "self.measure('{}', {}, '{}', {})\n".format(node.children[0].name, node.children[0].index,
                                                           node.children[1].name, node.children[1].index)
        self.add_text_with_indent(base)

    def get_args_from_indexedid(self, indexed_id):
        return "'" + indexed_id.name + "', " + str(indexed_id.index)

    @when(openqasmparser.node.reset.Reset)
    def visit(self, node):
        base = "self.set_qbit({}, 0)\n".format(self.get_args_from_indexedid(node.children[0]))
        self.add_text_with_indent(base)

    @when(openqasmparser.node.if_.If)
    def visit(self, node):
        base = "if self.conditional('{}', {}):\n".format(node.children[0].name, node.children[1].qasm())
        base += self.half_indent
        self.add_text_with_indent(base)
        node.children[2].accept(self)

    def add_text_with_indent(self, base):
        if not self.text:
            self.text += base
        else:
            self.text += self.indent + base

    @when(openqasmparser.node.barrier.Barrier)
    def visit(self, node):
        pass
    # dopisać dodanie jakiejś funkcji ewentualnie komentarza jakiegoś?
