
instruction_set = {
    'ADD': '18',
    'AND': '40',
    'COMP': '28',
    'DIV': '24',
    'J': '3C',
    'JEQ': '30',
    'JGT': '34',
    'JLT': '38',
    'JSUB': '48',
    'LDA': '00',
    'LDCH': '50',
    'LDL': '08',
    'LDX': '04',
    'MUL': '20',
    'OR': '44',
    'RD': 'D8',
    'RSUB': '4C',
    'STA': '0C',
    'STCH': '54',
    'STL': '14',
    'STSW': 'E8',
    'STX': '10',
    'SUB': '1C',
    'TD': 'E0',
    'TIX': '2C',
    'WD': 'DC'
}


symbol_table = {}
with open("SYMTAB.txt", "r") as symtab_file:
    for line in symtab_file:
        symbol, address = line.strip().split()
        symbol_table[symbol] = address


def binary_to_hex(binary):
    hex_value = hex(int(binary, 2))[2:].upper()
    return hex_value.zfill(6)


with open("program_info.txt", "r") as info_file:
    program_info = [line.strip().split(": ")[1] for line in info_file]

program_name = program_info[0]
start_address = int(program_info[3], 16)
program_length = int(program_info[1], 16)


with open("intermediatefile.mdt", "r") as infile, \
        open("listingFile.lst", "w") as outfile, \
        open("errorfile.txt", "w") as errorfile:
    for line_num, line in enumerate(infile, start=1):
        parts = line.strip().split("\t")
        if len(parts) < 3:
            errorfile.write(f"Incomplete line at line {line_num}\n")
            continue

        address, instruction, operand = parts

        if instruction in ['RESW', 'WORD', 'BYTE', 'RESB', 'END', 'START']:

            outfile.write(f"{address}\t{instruction}\t{operand}\n")
            continue

        if not operand:
            errorfile.write(f"Empty operand at line {line_num}\n")
            operand_address_binary = '0' * 15
        else:

            indexed = "1" if ",X" in operand else "0"
            operand = operand.split(",")[0]
            operand_address = symbol_table.get(operand)
            if operand_address is None:
                errorfile.write(
                    f"Undefined symbol: {operand} at line {line_num}\n")
                continue

            operand_address_binary = bin(int(operand_address, 16))[
                2:].zfill(15)

        opcode = instruction_set.get(instruction.strip())
        if opcode is None:
            errorfile.write(
                f"Undefined instruction: {instruction} at line {line_num}\n")
            continue

        opcode_binary = bin(int(opcode, 16))[2:].zfill(8)
        indexed_binary = indexed.zfill(1)

        object_code_binary = opcode_binary + indexed_binary + operand_address_binary

        object_code_hex = binary_to_hex(object_code_binary)

        outfile.write(
            f"{address}\t{instruction}\t{operand}\t{object_code_hex}\n")


object_file_content = []


header_record = f"H{program_name:<6}{start_address:06X}{program_length:06X}"
object_file_content.append(header_record)


current_address = start_address
current_record = ["T", f"{current_address:06X}", ""]
for line in open("listingFile.lst"):
    parts = line.strip().split("\t")
    if len(parts) >= 4:
        address, _, _, object_code = parts
        if len(current_record[2]) + len(object_code) <= 60:
            current_record[2] += object_code
        else:
            object_file_content.append("".join(current_record))
            current_address = int(address, 16)
            current_record = ["T", f"{current_address:06X}", object_code]
if current_record[2]:
    object_file_content.append("".join(current_record))


end_record = f"E{start_address:06X}"
object_file_content.append(end_record)


with open("object_file.obj", "w") as object_file:
    for line in object_file_content:
        object_file.write(line + "\n")
