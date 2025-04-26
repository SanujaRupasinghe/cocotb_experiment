import cocotb
from cocotb.triggers import Timer, RisingEdge
from tabulate import tabulate
import random

# log data to a list
log_data = []  

# save log data to a file
def save_log(filename="pipelined_test_2.txt", data_list=log_data):
    headers = ["reset", "in_a", "in_b", "in_c", "ready_out", "valid_in", "result", "valid_out", "ready_in", "valid_out_shift"]
    table = tabulate(data_list, headers=headers, tablefmt="plain")
    
    with open(filename, "w") as f:
        f.write(table)


# generate clock signals no logging
async def generate_clock(dut):
    while True:
        dut.clk.value = 0
        await Timer(1, units="ns")
        dut.clk.value = 1
        await Timer(1, units="ns")


# log data to a list
def log_signals_list(dut):
    global log_data
    row = [
        int(dut.reset.value),
        int(dut.in_a.value),
        int(dut.in_b.value),
        int(dut.in_c.value),
        int(dut.ready_out.value),
        int(dut.valid_in.value),
        int(dut.result.value),
        int(dut.valid_out.value),
        int(dut.ready_in.value),
        format(int(dut.valid_out_reg_shift.value), '04b')
    ]
    log_data.append(row)


# insert random values to model and compare predicted/ expected value vs actual value
@cocotb.test()
async def pipeline_test_2(dut):
    cocotb.start_soon(generate_clock(dut))

    dut.ready_in.value = 1     #always ready to accept output data from the module 

    for i in range(50): 
        await RisingEdge(dut.clk)

        if i == 0 or i == 20:
            dut.reset.value = 1
        else:
            dut.reset.value = 0 

        dut.in_a.value = random.randint(0, 2**8 - 1)
        dut.in_b.value = random.randint(0, 2**8 - 1)
        dut.in_c.value = random.randint(0, 2**8 -1)
        dut.valid_in.value = random.choices([1, 0], weights=[90, 10])[0]  # 80% of valid_ins are 1

        # Call log function to store values
        log_signals_list(dut)

    # iterate through logged data if the ouptput is valid, then compare
    for item in range(5, len(log_data)):
        if (log_data[item][7] == 1):   
            dut._log.info(f"calculated by DUT= {log_data[item][6]}, expected = {log_data[item-4][1] * log_data[item-4][2] + log_data[item-4][3]}")
            assert (log_data[item][6] == log_data[item-4][1] * log_data[item-4][2] + log_data[item-4][3]), "Error in calculation"

    # Save data to file after the test
    save_log("pipeline_test_2.txt", log_data)  

    dut._log.info("pipeline_test_2 Test completed.")
