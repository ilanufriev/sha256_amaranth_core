import cocotb
import random
import hashlib
import time
import sys
import os

from cocotb.triggers import Timer
from datetime import datetime


RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
RESET = "\033[0m"

async def gen_clk(clk_port, count: int):
    for _ in range(0, count):
        clk_port.value = 0
        await Timer(1, unit="ns")
        clk_port.value = 1
        await Timer(1, unit="ns")

    return count


def bytes_to_block(byte_list: bytes, length):
    block = 0x00

    for i in range(length):
        block |= byte_list[length - 1 - i] << (i * 8)

    return block


def pad(message: bytes, message_byte_length: int):
    padded_bytes = [b for b in message]
    padded_length = -1
    message_bit_length = message_byte_length * 8

    if (message_byte_length % 64) < 56:
        padded_length = message_byte_length + 56 - (message_byte_length % 64) + 8
    else:
        padded_length = message_byte_length + 64 + 56 - (message_byte_length % 64) + 8

    padded_bytes.append(0x80)

    while len(padded_bytes) < (padded_length - 8):
        padded_bytes.append(0x00)

    for i in range(0, 8):
        padded_bytes.append((message_bit_length >> ((7 - i) * 8)) & 0xFF)

    return padded_bytes


async def hash_sha256(dut, block):
    clks = 0
    dut.block_i.value = block
    dut.valid_i.value = 1

    await gen_clk(dut.clk, 1)

    while dut.valid_i.value == dut.ready_o.value:
        clks += await gen_clk(dut.clk, 1)

    dut.valid_i.value = 0

    while dut.ready_o.value == 0:
        clks += await gen_clk(dut.clk, 1)

    return clks


def assert_eq(val, expected):
    if val != expected:
        raise AssertionError(f"Assertion failed. Expected {expected!r}, got {val!r}")


async def run_test(dut, message):
    clks = 0

    padded_message = pad(message, len(message))
    assert_eq(len(padded_message) % 64, 0)
    golden = hashlib.sha256()
    golden.update(message)
    golden_result = golden.hexdigest()
    assert_eq(len(padded_message) % 64, 0)

    # reset first

    dut.rst.value = 1

    await gen_clk(dut.clk, 10)

    dut.rst.value = 0

    await gen_clk(dut.clk, 3)

    is_first = True
    while len(padded_message) >= 64:
        if is_first:
            dut.first_i.value = 1
            is_first = False
        else:
            dut.first_i.value = 0

        block = bytes_to_block(padded_message, 64)
        cocotb.log.info("block: %0x", block)
        padded_message = padded_message[64:]
        clks += await hash_sha256(dut, block)
        result = dut.hash_o.value

    hex_result = hex(result)[2:]
    while len(hex_result) < 64:
        hex_result = "0" + hex_result

    cocotb.log.info("Golden: %s", golden_result)
    cocotb.log.info("HDL   : %s", hex_result)
    assert_eq(hex_result, golden_result)
    cocotb.log.info(f"{GREEN}PASS!{RESET}")

    return clks


seed = time.time_ns()
random.seed(1772281687411028689)


@cocotb.test()
async def empty_message(dut):
    await run_test(dut, bytes([]))

@cocotb.test()
async def block_limit64(dut):
    await run_test(dut, bytes(i & 0xff for i in range(0, 64)))


@cocotb.test()
async def block_limit63(dut):
    await run_test(dut, bytes(i & 0xff for i in range(0, 63)))


@cocotb.test()
async def block_limit56(dut):
    await run_test(dut, bytes(i & 0xff for i in range(0, 56)))


@cocotb.test()
async def block_limit55(dut):
    await run_test(dut, bytes([i & 0xff for i in range(0, 55)]))


@cocotb.test()
async def random_messages(dut):
    date = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    filename = f"measurements.log"
    with open(filename, "w") as f:
        f.write("Clock count,Message size (bytes),Throughput (bytes/clk)\n")
        for test_case in range(1, 10):
            byte_count = random.randint(0, 300)
            message = random.randbytes(byte_count)
            total_byte_count = len(pad(message, len(message)))

            cocotb.log.info("--- test case %d ---", test_case)
            cocotb.log.info("   seed: %d", seed)
            cocotb.log.info("   message length: %d", len(message))

            clks = await run_test(dut, message)

            f.write(f"{clks},{total_byte_count},{total_byte_count/clks:.03f}\n")
