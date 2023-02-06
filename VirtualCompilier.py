links = []

def decode(command,step):
    inputs = command.split()
    if inputs[0][-1] == ':':
        inputs = inputs[1:]
    if inputs[0] != "RET":
        registers = inputs[1].split(",")
    else:
        registers = []
    if len(registers) > 2:
        imm = isimm(registers[2])
    elif inputs[0] == "MOV":
        imm = isimm(registers[1])
    else:
        imm = 0
    action = findaction(inputs[0],imm)
    if inputs[0] == "B":
        imm11 = branchImm(registers[0],step)
        output = action+imm11+"00000"+"00000"
    elif inputs[0] == "BL":
        links.append(step)
        imm11 = branchImm(registers[0],step)
        output = action+imm11+"00000"+"00111"
    elif inputs[0] == "CBZ":
        imm11 = branchImm(registers[1],step)
        Rt = fivebit(numToBi(int(registers[0][1:])))
        output = action+imm11+"00000"+Rt
    elif inputs[0] == "RET":
        y = links.pop(-1)
        imm11 =  "1"+elevenbit(numToBi(step-y))[1:]
        output = action+imm11+"00000"+"11110"
    elif inputs[0] == "B.EQ":
        imm11 = branchImm(registers[0],step)
        output = action+imm11+"00000"+"00000"
    elif inputs[0] == "MOV":
        if imm == 0:
            Rd = fivebit(numToBi(int(registers[0][1:])))
            Rn = Rd
            Rm = fivebit(numToBi(int(registers[1][1:])))
            output = action+Rm+"111000"+Rn+Rd
        else:
            if registers[1][0] == "-":
                imm11 = negative(elevenbit(numToBi(int(registers[1][1:]))))
            else:
                imm11 = elevenbit(numToBi(int(registers[1])))
            Rd = fivebit(numToBi(int(registers[0][1:])))
            Rn = Rd
            output = action+imm11+Rn+Rd
    elif inputs[0] == "LDR" or inputs[0] == "STR":
        if len(registers) == 2:
            imm11 = "00000000000"
            Rn = fivebit(numToBi(int(registers[1][2:-1])))
        else:
            if registers[2][0] == "-":
                imm11 = negative(elevenbit(numToBi(int(registers[2][1:]))))
            else:
                imm11 = elevenbit(numToBi(int(registers[2][:-1])))
            Rn = fivebit(numToBi(int(registers[1][2:])))
        Rt = fivebit(numToBi(int(registers[0][1:])))
        output = action+imm11+Rn+Rt            
    else:
        Rn = fivebit(numToBi(int(registers[1][1:])))
        Rd = fivebit(numToBi(int(registers[0][1:])))
        if imm == 0:
            Rm = fivebit(numToBi(int(registers[2][1:])))
            output = action+Rm+"111000"+Rn+Rd
        else:
            if registers[2][0] == "-":
                imm11 = negative(elevenbit(numToBi(int(registers[2][1:]))))
            else:
                imm11 = elevenbit(numToBi(int(registers[2])))
            output = action+imm11+Rn+Rd
    return ninebit(biToHex(output)[2:])
            
def findaction(action,imm):
    if action == "AND":
        if imm == 0:
            return "0000000000001"
        else:
            return "000000001001001"
    if action == "ANDS":
        if imm == 0:
            return "100000010001001"
        else:
            return "100000011001001"
    if action == "ORR":
        if imm == 0:
            return  "000100000001001"
        else:
            return "000100001001001"
    if action == "ORRS":
        if imm == 0:
            return "100100010001001"
        else:
            return "100100011001001"
    if action == "ADD":
        if imm == 0:
            return "001000000001001"
        else:
            return "101000001001001"
    if action == "ADDS":
        if imm == 0:
            return "001000010001001"
        else:
            return "101000011001001"
    if action == "SUB":
        if imm == 0:
            return "001100000001001"
        else:
            return "001100001001001"
    if action == "SUBS":
        if imm == 0:
            return "101100010001001"
        else:
            return "101100011001001"
    if action == "MUL":
        if imm == 0:
            return "010000000001001"
        else:
            return "010000001001001"
    if action == "DIV":
        if imm == 0:
            return "010100000001001"
        else:
            return "010100001001001"
    if action == "LDR":
        return "001000001011010"
    if action == "STR":
        return "001000001100000"
    if action == "B":
        return "011100100000100"
    if action == "BL":
        return "011100110001000"
    if action == "CBZ":
        return "011101010000000"
    if action == "RET":
        return "011110010000000"
    if action == "B.EQ":
        return "011101010000000"
    if action == "MOV":
        if imm == 0:
            return "011100000001001"
        else:
            return "011100001001001"

def fivebit(register):
    if len(register) == 5:
        return register
    elif len(register) < 5:
        return fivebit("0" + register)
    else:
        return fivebit(register[1:])
    
def elevenbit(register):
    if len(register) == 11:
        return register
    elif len(register) < 11:
        return elevenbit("0" + register)
    else:
        return elevenbit(register[1:])
    
def numToBi(num):
    if num == 0: return ""
    elif (num % 2 == 1): return numToBi((num-1)/2) + "1"
    else: return numToBi(num/2) + "0"

def isimm(register):
    if register[0].isnumeric():
        return 1
    elif register[0] == "-":
        return 1
    else:
        return 0

def branchImm(register,step):
    y = 0
    found = 0
    with open('commands.txt') as f:
        while found == 0:
            command= f.readline()
            if command != "":
                inputs = command.split()
                if inputs[0][:-1] == register:
                    found = 1
                else:
                    y += 1
            else:
                y+=1
    if y > step:
        return elevenbit(numToBi(y-step))
    else:
        return "1" + elevenbit(numToBi(step-y))[1:]
        

def biToHex(num):
    return hex(int(num,2))

def fourbit(num):
    if len(num) == 4:
        return num
    elif len(num) < 4:
        return fourbit("0" + num)
    else:
        return fourbit(num[1:])

def ninebit(num):
    if len(num) == 9:
        return num
    elif len(num) < 9:
        return ninebit("0" + num)
    else:
        return ninebit(num[1:])

def negative(binary):
    i = 0
    num = ""
    while i < len(binary) and binary[i] == "0":
        num += "1"
        i+=1
    num += binary[i:]
    return num

with open('commands.txt') as f:
    step = 0
    command = f.readline()
    with open('CPURAMmem', 'w') as g:
        g.write("v3.0 hex words addressed\n")
        while step <= 65535:
            if command != "":
                if step % 8 == 0:
                    g.write(fourbit(hex(step)[2:])+": "+decode(command,step)+" ")
                    command = f.readline()
                    step += 1
                elif (step + 1) % 8 == 0:
                    g.write(decode(command,step)+"\n")
                    command = f.readline()
                    step += 1
                else:
                    g.write(decode(command,step)+" ")
                    command = f.readline()
                    step += 1
            else:
                if step % 8 == 0:
                    g.write(fourbit(hex(step)[2:])+": 000000000 ")
                    step += 1
                elif (step + 1) % 8 == 0:
                    g.write("000000000\n")
                    step += 1
                else:
                    g.write("000000000 ")
                    step += 1
