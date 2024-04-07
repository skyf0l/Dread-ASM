# Dread-ASM

The all-in-one assembly language that can be natively executed on all modern satellites!

The Dread-ASM is a custom assembly language created by [DreadFog](https://github.com/DreadFog) for the [THCon CTF 2024](https://thcon.party/). Here is my implementation of the Dread-ASM interpreter in Python.

## Challenge

### Dread-ASM - Part 1

```console
$ python Dread-ASM.py chall1.dreadasm
Buffer content: b'THCON{1nT3rPR3ter5_4r3_FUN!!!!!}'
```

The flag is `THCON{1nT3rPR3ter5_4r3_FUN!!!!!}`.

### Dread-ASM - Part 2

```console
$ python Dread-ASM.py chall2.dreadasm
Enter a number: 10
Buffer content: b"This is not the flag, i'm sorry!"
$ python Dread-ASM.py chall2.dreadasm
Enter a number: 84
Enter a number: 42
Buffer content: b"This is not the flag, i'm sorry!"
$ python Dread-ASM.py chall2.dreadasm 84 72 67 79 78 123 121 48 117 95 71 117 51 53 115 51 100 95 109 51 95 99 48 82 114 51 99 55 108 89 33 125
Buffer content: b"Congratulations! It's the flag!!"
```

The flag is `THCON{y0u_Gu35s3d_m3_c0Rr3c7lY!}` (from ASCII values).

## Architecture

Luckily, one of the developers has kept the manual referencing all the opcodes.

Here is the manual:

```plaintext
## Version: 0.7.0

### Registers

the usual RIP to count instructions
R0 and R1 registers for calculus
LCT is the loop count register. It keeps the index of the current loop within the program
PTR is a register that keeps a pointer to one of the cells of the buffer

### The holy buffer

This super duper cool architecture has a whole 32\*8 bit buffer, capable of holding up to 32 8-bit integers! Some may argue that it isn't enough, but it's only because their code isn't optimized enough!

### Basic operations

ADD R1 R2 : R1 <- (R1 + R2) % 0xff
MOV R1 cst : R1 <- cst
XOR R1 R2 : R1 <- R1 ^ (R2 + 3) % 0xff and no, this is not a bug, it's a feature!
CMP R1 R2 : classic comparison between R1 and R2
CLP cst: classic comparison between LCT and cst

### Flow control

three flags : is_bigger, is_equal and is_smaller
JRA cst : rip <- rip + cst ; you can read this opcode "jump relative always"
JRG cst : rip <- rip + cst if is_bigger flag set ; it reads "jump relative greater"
JRE cst : rip <- rip + cst if is_equal flag set ; it reads "jump relative equal"
JRL cst : rip <- rip + cst if is_smaller flag set ; it reads "jump relative lower"
INL cst: LCT = cst
ICL : LCT += 1
SPL: PTR = LCT

### Pointers and data

LDA : R0 <- buf[PTR]
IPT : PTR <- (PTR + 3) % 32 ; The boss Jeb really wanted this feature, so here it is --'
LPT RI : RI <- PTR
STD RI : buf[PTR] <- RI

### Additional properties

The buffer is initialized with only zeroes.
All registers are initialized with a value equal to 1, except rip which starts at 0.
The comparison flags are set to True by default

## Version 1.0.0

### Registers

R2 joins the party as a calculus buffer! It is also initialized to 1

### User input

RDV : R0 <- int(user_input)
PBF : print the buffer

### Execution termination

HLT : exit the program
```
