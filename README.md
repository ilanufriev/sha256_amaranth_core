# sha256\_amaranth\_core

SHA-256 hash function Amaranth HDL implementation.

## Usage

There are two ways to use this core. If you use Amaranth HDL in your projects, then you can just import this core and use it as any other Amaranth HDL component. If you want to use it in your Verilog HDL project, then run the .py file directly:

```
python3 sha256.py
```

This will generate sha256.v in the same directory. It then can be included in your project.

## Testing

First, generate a Verilog module from Amaranth HDL description:

```
python3 sha256.py
```

Then, go into "tb" directory and run make:

```
cd tb && make
```

This will run necessary test cases and report their results.

## Implementation details

Implemented using Xilinx Vivado 2018.1 for Artix-7 (model name: 7a100tcsg324-3)

- LUTs: 1312
- FFs: 1290
- Latency: 67 cycles
- Frequency: 100MHz

## Big thanks to

Special thanks to amazing projects and people:

 - [Joachim Strömbergson](https://github.com/secworks) - his sha256 core is the main inspiration for this implemetation.
 - [Amarantah HDL](https://github.com/amaranth-lang/amaranth) - HDL that was used to create this core.
 - [cocotb](https://github.com/cocotb/cocotb) - cocotb is a verification framework that allows users to write VHDL and Verilog testbenches in Python.
