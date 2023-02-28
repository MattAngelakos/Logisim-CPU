```
The Virtual CPU Manual
```
**Names:** Matthew Angelakos and Elliot Niemann

**Pledge:** I pledge my honor that I have abided by the Stevens Honor System.

**Question:** What did each of us do?

**Answer:** To make this simple

- General Outline: Both
- Encoding System: Both
- CPU: Matthew
- Assembler: Elliot

# Assembler Information:

- Use the program in the same folder as the text file named “commands.txt” that
    contains the instructions.
- Runs through all needed commands when run
- Reads through the text file and outputs image file “CPURAMmem.”
- The image file is then loaded into the RAM in the CPU

# CPU Information:

- 7 General Registers, 1 Link Register(Can just be used as a General Register as
    well). From X0-X6(General), X7(Link), Everything 16bit
- 16 Bit instructions(You can make 65k instructions if you wanted!)
- Each register can be referenced like in a regular Armx86 assembly with the X in
    front followed by the number, i.e., X2.
- Pipelined, no control or data hazard.
- What instructions can we give? (imm) = immediate useable as well, (Z)=can set the
    Zero flag, All do the same as in standard ARM
       - LDR: Loads data from memory at address Xn offset by an imm
       - STR: Stores data in the memory at address Xt offset by an imm


- MOV(imm) moves data into a register
- ADD(imm)(Z) adds data together and puts it into a register
- SUB(imm)(Z) subtracts data together and puts it into a register
- MUL(imm)(Z) multiplies data together and puts it into a register
- DIV(imm)(Z) divides data together and puts it into a register
- AND(imm)(Z) takes the logical and of two data and puts it into a register
- ORR(imm)(Z) takes the logical or of two data and puts it into a register
- B branches to an instruction indicated by the label
- CBZ branches to an instruction indicated by the label if = 0
- BL branches to an instruction indicated by the label and puts the current
    address into the Link Register
- RET returns the PC to whatever is in the Link Register

# Encoding:

Our system uses a 36-bit encoding scheme, based on what we reviewed in class, and an
extra 4 for what to do inside the ALU. So that is why every field’s size is based on the
textbook. Note this could've been shortened, but we wanted not to have an issue adding
more instructions or registers, and we knew what was used in the textbook could
implement everything I’d like to add; MemRead also could've been removed, but we
didn’t think we’d make it line address and not byte address. If it's hard to read above, we
also attached the text file in our submission under codes.txt.


# Instructions Format:

AND Rd,Rn,Rm / AND Rd,Rn,imm  
ANDS Rd,Rn,Rm / ANDS Rd,Rn,imm  
ORR Rd,Rn,Rm / ORR Rd,Rn,imm  
ORRS Rd,Rn,Rm / ORRS Rd,Rn,imm  
ADD Rd,Rn,Rm / ADD Rd,Rn,imm  
ADDS Rd,Rn,Rm / ADDS Rd,Rn,imm  
SUB Rd,Rn,Rm / SUB Rd,Rn,imm  
SUBS Rd,Rn,Rm / SUBS Rd,Rn,imm  
MUL Rd,Rn,Rm / MUL Rd,Rn,imm  
DIV Rd,Rn,Rm / DIV Rd,Rn,imm  
LDR Rt,[Rn] / LDR Rt,[Rn,imm11]  
STR Rt,[Rn] / STR Rt,[Rn,imm11]  
B label  
BL label  
CBZ Rt,label  
RET  
B.EQ label  
MOV Rd, Rm / MOV Rd,imm  
When the labeling line is to be branched to the format is “(label): ” before the command.  

# How to use:
1. Download AngelakosVirtual.circ and VirtualCompilier.py.
2. Have Logisim-Evolution and at least Python 3.0 installed.
3. Follow the directions here or in VirtualManual.pdf to write the code for your program in the VirtualCompilier.py.
4. Run the VirtualCompilier.py to recieve the machine code for your instructions.
5. Start Logisim and load the CPU using File -> Open and selecting AngelakosVirtual.circ.
6. Load the instructions into the top RAM by right-clicking on the address box and clicking load image and select the file that the compiler just produced. 
7. If you wish you can write whichever data you like into the other RAM for your program. Unfortunately our compilier only supports instruction compiliation.
8. Click "Simulate" at the top of Logisim and click "Auto-Tick Enabled".
9. Watch your program run.