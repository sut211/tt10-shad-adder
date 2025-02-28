# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test project behavior")

    # Test Case 1:
    # Combined input: uio_in = 0x2A (00101010), ui_in = 0xF1 (11110001)
    # Expected: First '1' from the top is at bit position 13.
    dut.uio_in.value = 0x2A  # upper 8 bits
    dut.ui_in.value  = 0xF1  # lower 8 bits
    await ClockCycles(dut.clk, 1)
    assert int(dut.uo_out.value) == 13, f"Test Case 1 failed: Expected 13, got {int(dut.uo_out.value)}"

    # Test Case 2:
    # Combined input: 0x0001 (uio_in = 0x00, ui_in = 0x01)
    # Expected: First '1' is at bit position 0.
    dut.uio_in.value = 0x00
    dut.ui_in.value  = 0x01
    await ClockCycles(dut.clk, 1)
    assert int(dut.uo_out.value) == 0, f"Test Case 2 failed: Expected 0, got {int(dut.uo_out.value)}"

    # Test Case 3:
    # Combined input: 0x0000 (all zeros)
    # Expected: Special case output 0xF0.
    dut.uio_in.value = 0x00
    dut.ui_in.value  = 0x00
    await ClockCycles(dut.clk, 1)
    assert int(dut.uo_out.value) == 0xF0, f"Test Case 3 failed: Expected 0xF0, got {int(dut.uo_out.value)}"

    # Test Case 4:
    # Combined input: 0x8000 (uio_in = 0x80, ui_in = 0x00)
    # Expected: First '1' is at bit position 15.
    dut.uio_in.value = 0x80  # 10000000
    dut.ui_in.value  = 0x00  # 00000000
    await ClockCycles(dut.clk, 1)
    assert int(dut.uo_out.value) == 15, f"Test Case 4 failed: Expected 15, got {int(dut.uo_out.value)}"

    dut._log.info("All tests passed!")
