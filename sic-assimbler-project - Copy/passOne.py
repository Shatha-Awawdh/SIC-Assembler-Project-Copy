from tabulate import tabulate

SourceCode = "sourcecode.txt"
IntermediateFile = 'intermediatefile.mdt'
InstructionSet = 'instructionSet.txt'
ErrorFile = 'errorfile.txt'
ProgramInfoFile = 'program_info.txt'
SYMTABFile = 'SYMTAB.txt'
OPTABFile = 'OPTAB.txt'
symbol_table_rows = []
object_table_rows = []

directives = ['START', 'END', 'BYTE', 'WORD', 'RESB', 'RESW']

instructionSet = {}
with open(InstructionSet, 'r') as instr_file:
    for line in instr_file:
        instruction, opcode = line.strip().split()
        instructionSet[instruction] = opcode


def print_error_message(line_num, message):
    error_message = f"Pass 1 Error at line {line_num}: {message}\n"
    print(error_message)
    with open(ErrorFile, 'a') as error_file:
        error_file.write(error_message)


with open(SourceCode, "r") as file, open(IntermediateFile, 'w') as intermediate_file:
    line_num = 1
    line = file.readline().strip()
    STARTADR = 0
    LOCCTR = 0
    if line[11:20].strip() == "START":
        STARTADR = int(line[21:39].strip(), 16)
        LOCCTR = STARTADR
        symbol_table_rows.append([line[:10].strip(), hex(LOCCTR).upper()])
        PRGNAME = line[0:10].strip()
    line = file.readline().strip()
    while line:
        print(f"Processing line {line_num}: {line}")
        if line[11:20].strip() == "END":
            break

        if not line.startswith('.'):
            operation_code_or_directive = line[11:20].strip()
            # Debugging print
            print(
                f"Operation code or directive: {operation_code_or_directive}")

            if operation_code_or_directive not in directives and operation_code_or_directive not in instructionSet:
                print_error_message(
                    line_num, "Invalid operation code or directive")
                exit(-1)

            operand = line[21:39].strip()
            print(f"Operand: {operand}")

            if operation_code_or_directive not in directives:
                object_table_rows.append(
                    [operation_code_or_directive, hex(LOCCTR).upper()])

            if line[0:10].strip() != "-":
                SYMBOL = line[0:10].strip()
                if SYMBOL in instructionSet or SYMBOL in directives:
                    print_error_message(
                        line_num, f"Symbol '{SYMBOL}' found in instruction set or directives")
                    exit(-1)
                if SYMBOL in [row[0] for row in symbol_table_rows]:
                    print_error_message(line_num, "Duplicated Symbol")
                    exit(-1)
                symbol_table_rows.append([SYMBOL, hex(LOCCTR).upper()])

            intermediate_file.write(
                f"{hex(LOCCTR).upper()}\t{operation_code_or_directive.upper()}\t{operand.upper()}\n")

            if operation_code_or_directive == 'WORD':
                LOCCTR += 3
            elif operation_code_or_directive == 'RESW':
                LOCCTR += 3 * int(operand)
            elif operation_code_or_directive == 'RESB':
                LOCCTR += int(operand)
            elif operation_code_or_directive == 'BYTE':
                XORC = line[22:23].strip()
                if XORC == 'X':
                    operandValue = operand.split("'")[1]
                    LOCCTR += (len(operandValue) / 2)
                elif XORC == 'C':
                    operandValue = operand.split("'")[1].encode().hex()
                    LOCCTR += (len(operandValue) / 2)
            else:
                LOCCTR += 3

        line = file.readline().strip()
        line_num += 1

# Write program information to program_info.txt
with open(ProgramInfoFile, 'w') as program_info_file:
    program_info_file.write(f"Program Name: {PRGNAME.upper()}\n")
    program_info_file.write(
        f"Program Length: {hex(LOCCTR - STARTADR).upper()}\n")
    program_info_file.write(f"Location Counter: {hex(LOCCTR).upper()}\n")
    program_info_file.write(f"Start Address: {hex(STARTADR).upper()}\n")

# Write symbol table to SYMTAB.txt
with open(SYMTABFile, 'w') as symtab_file:
    for row in symbol_table_rows:
        symtab_file.write(f"{row[0]} {row[1]}\n")

# Write object table to OPTAB.txt
with open(OPTABFile, 'w') as optab_file:
    for row in object_table_rows:
        optab_file.write(f"{row[0]} {row[1]}\n")

programLength = hex(LOCCTR - STARTADR).upper()
print('Program Name: ', PRGNAME.upper())
print('Program Length:', programLength)
print('Location Counter: ', hex(LOCCTR).upper())
print('Start Address:', hex(STARTADR).upper())
