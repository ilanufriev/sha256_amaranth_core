# SHA256 C

Functional model of the SHA256 hashing algorithm written in C. If Amaranth HDL description looks too unfamiliar, try looking at this first, I've made my best to keep this version readeable while also maintaining core principles and tricks that were used in hardware implementation of this algorithm.

## Compiling

No dependencies except gcc and libc are required. Compile this with:

```
make
```

And then run:

```
./sha256_cli
```

To see help.

## Basic usage

Basic usage is very simple. One way to get the hash of a file is by piping its contents to sha256\_cli:

```
cat Makefile | ./sha256_cli
```

Another way is by using an "-f" flag:

```
./sha256_cli -f Makefile
```

By default hash is displayed in big-endian format. If you want it to be displayed in raw format, use "-l" flag:

```
./sha256_cli -l -f Makefile
```

This implementation of the algorithm was not made for devices that store numbers in big-endian format. I can't and will not guarantee that it will work on these systems.
