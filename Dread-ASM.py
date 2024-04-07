#!/usr/bin/env python3

from sys import argv
from typing import Generator

if len(argv) < 2:
    print("Usage: python3 Dread-ASM.py <file> [inputs...]")
    exit(1)


BUFFER_SIZE = 32


def parse_cst(cst: str) -> int:
    '''
    Parse a constant from the format !{cst}
    '''

    if cst[0] == '!' and cst[1] == '{' and cst[-1] == '}':
        return int(cst[2:-1])

    raise ValueError(f"Invalid constant: {cst}")


def run(program: list[str], inputs: Generator[int, None, None]):
    registers = {
        "RIP": 0,  # Instruction Counter
        "R0": 1,  # Used for calculations
        "R1": 1,  # Used for calculations
        "R2": 1,  # Used for calculations
        "LCT": 0,  # Loop Counter
        "PTR": 0,  # Pointer to buffer
    }

    # Flags
    isBigger = True
    isEqual = True
    isSmaller = True

    buffer = [0] * BUFFER_SIZE

    while True:

        # End of program
        if registers['RIP'] >= len(program):
            break

        # Parse instruction
        instruction = program[registers['RIP']].split(' ')

        # Used to increment RIP
        incRip = 1

        # Basic operations
        if instruction[0] == 'ADD':
            registers[instruction[1]] = (
                registers[instruction[1]] + registers[instruction[2]]) % 0xff
        elif instruction[0] == 'MOV':
            registers[instruction[1]] = parse_cst(instruction[2])
        elif instruction[0] == 'XOR':
            registers[instruction[1]] = registers[instruction[1]] ^ (
                registers[instruction[2]] + 3) % 0xff
        elif instruction[0] == 'CMP':
            if registers[instruction[1]] > registers[instruction[2]]:
                isBigger = True
                isEqual = False
                isSmaller = False
            elif registers[instruction[1]] == registers[instruction[2]]:
                isBigger = False
                isEqual = True
                isSmaller = False
            else:
                isBigger = False
                isEqual = False
                isSmaller = True
        elif instruction[0] == 'CLP':
            if registers['LCT'] > parse_cst(instruction[1]):
                isBigger = True
                isEqual = False
                isSmaller = False
            elif registers['LCT'] == parse_cst(instruction[1]):
                isBigger = False
                isEqual = True
                isSmaller = False
            else:
                isBigger = False
                isEqual = False
                isSmaller = True

        # Flow control
        elif instruction[0] == 'JRA':
            incRip = parse_cst(instruction[1])
        elif instruction[0] == 'JRG':
            if isBigger:
                incRip = parse_cst(instruction[1])
        elif instruction[0] == 'JRE':
            if isEqual:
                incRip = parse_cst(instruction[1])
        elif instruction[0] == 'JRL':
            if isSmaller:
                incRip = parse_cst(instruction[1])
        elif instruction[0] == 'INL':
            registers['LCT'] = parse_cst(instruction[1])
        elif instruction[0] == 'ICL':
            registers['LCT'] += 1
        elif instruction[0] == 'SPL':
            registers['PTR'] = registers['LCT']

        # Pointers and data
        elif instruction[0] == 'LDA':
            registers['R0'] = buffer[registers['PTR'] % BUFFER_SIZE]
        elif instruction[0] == 'IPT':
            registers['PTR'] = (registers['PTR'] + 3) % BUFFER_SIZE
        elif instruction[0] == 'LPT':
            registers[instruction[1]] = registers['PTR']
        elif instruction[0] == 'STD':
            buffer[registers['PTR'] % BUFFER_SIZE] = registers[instruction[1]]

        # User input
        elif instruction[0] == 'PBF':
            print("Buffer content:", bytes(buffer))
        elif instruction[0] == 'RDV':
            registers['R0'] = next(inputs, None) or int(
                input("Enter a number: "))

        # Execution termination
        elif instruction[0] == 'HLT':
            break

        # Other
        elif instruction[0] == 'EOF':
            pass

        else:
            print("Invalid instruction:", instruction)

        # Increment RIP
        registers['RIP'] += incRip


def main():
    program = open(argv[1]).read().strip().split('\n')
    inputs = (i for i in map(int, argv[2:]))
    run(program, inputs)


if __name__ == "__main__":
    main()
