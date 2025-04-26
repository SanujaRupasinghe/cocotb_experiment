import cocotb
from cocotb.triggers import Timer, RisingEdge
from tabulate import tabulate

# generate clock signals with logging at each posedge
async def generate_clock_verbose(dut):
    while True:
        dut.clk.value = 0
        await Timer(1, units="ns")
        dut.clk.value = 1
        await Timer(1, units="ns")
        log_signals(dut)  # Log signal data at rising edge

# print log data at each posedge (print)
def log_signals(dut):
    """Log all relevant DUT signals."""
    dut._log.info(
        f"reset={dut.reset.value}, "
        f"in_a,b,c={int(dut.in_a.value)}, "
        f"result={int(dut.result.value)}, "
        f"valid_in={dut.valid_in.value}, "
        f"ready_out={dut.ready_out.value}, "
        f"valid_out={dut.valid_out.value}, "
        f"ready_in={dut.ready_in.value}, "
        f"valid_out_reg_shift={dut.valid_out_reg_shift.value}"
    )


# basic test to check if the module is working as expected by providing some input values and observing the output
@cocotb.test()
async def pipeline_test_1(dut):
    cocotb.start_soon(generate_clock_verbose(dut)) 

    dut.ready_in.value = 1     

    for i in range(20): 
        await RisingEdge(dut.clk)

        if i == 10 or i == 0:
            dut.reset.value = 1
        else:
            dut.reset.value = 0 

            
        dut.valid_in.value = 1
        dut.in_a.value = i + 10
        dut.in_b.value = i + 10
        dut.in_c.value = i + 10

    dut._log.info("pipeline_test_1 Test completed.")