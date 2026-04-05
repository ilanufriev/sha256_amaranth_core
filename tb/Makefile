WAVES ?= 1

TEST_MODULE ?= $(PWD)/../sha256.v

SIM ?= icarus
TOPLEVEL_LANG ?= verilog

VERILOG_SOURCES += $(TEST_MODULE)
COCOTB_TOPLEVEL ?= sha256
COCOTB_TEST_MODULES ?= test_sha256
include $(shell cocotb-config --makefiles)/Makefile.sim
