OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
creg c[3];
h q[1];
h q;
x q;
barrier q;
x q[2];
reset q[0];
ccx q[0],q[1],q[2];
if(c==3) x q[2];
cx q[1],q[2];
measure q[0] -> c[0];
measure q[1] -> c[1];
measure q[2] -> c[2];