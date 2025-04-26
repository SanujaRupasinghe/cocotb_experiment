SIM ?= verilator
TOPLEVEL_LANG ?= verilog

VERILOG_SOURCES += $(PWD)/pipelined_mul_acc.sv


# TOPLEVEL is the name of the toplevel module in your Verilog or VHDL file
TOPLEVEL = pipelined_mul_acc

# MODULE is the basename of the Python test file
MODULE = test_pipeline_2

EXTRA_ARGS += --trace

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim
