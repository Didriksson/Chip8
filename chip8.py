class chip8(object):
    def __init__(self):
        # As per chip8 specs PC starts per default at address 512.
        self.PC = 0x200
        self.I = bytearray(2)

        self.registers = bytearray(16)

        self.memory = bytearray(4096)
        self.opcodes = {
            0x1: self.jumpToAddress,
            0x3: self.skipNextInstructionIfVXEqualsNN,
            0x4: self.skipNextInstructionIfVXDoesNotEqualsNN,
            0x5: self.skipNextInstructionIfVXEqualsVY,
            0x6: self.setVXToNN,
            0x7: self.addVXToNN,
            0x8: self.logicalOperation
        }

        self.logicalOperations = {
            0x0: self.setVXToVY,
            0x1: self.setVXToVXorVY,
            0x2: self.setVXToVXandVY,
            0x3: self.setVXToVXxorVY,
            0x4: self.addVYToVX,
            0x5: self.subtractVYFromVX,
            0x6: self.shiftVXRight,
            0x7: self.subtractVXFromVYPlaceInVX,
            0xE: self.shiftVXLeft
        }

    def logicalOperation(self, operand):
        self.logicalOperations[operand & 0x000F](operand)

    def jumpToAddress(self, operand):
        self.PC = operand & 0x0FFF

    def skipNextInstructionIfVXEqualsNN(self, operand):
        registerToCheck = operand >> 8 & 0xF
        if self.registers[registerToCheck] == (operand & 0xFF):
            self.PC += 2

    def skipNextInstructionIfVXDoesNotEqualsNN(self, operand):
        registerToCheck = operand >> 8 & 0xF
        if self.registers[registerToCheck] != (operand & 0xFF):
            self.PC += 2

    def skipNextInstructionIfVXEqualsVY(self, operand):
        register1 = operand >> 8 & 0xF
        register2 = operand >> 4 & 0xF
        if self.registers[register1] == self.registers[register2]:
            self.PC += 2

    def setVXToNN(self, operand):
        register = operand >> 8 & 0xF
        value = operand & 0xFF
        self.registers[register] = value

    def addVXToNN(self, operand):
        register = operand >> 8 & 0xF
        value = operand & 0xFF
        self.registers[register] += value

    def setVXToVY(self, operand):
        register1 = operand >> 8 & 0xF
        register2 = operand >> 4 & 0xF
        self.registers[register1] = self.registers[register2]

    def setVXToVXorVY(self, operand):
        reg1 = operand >> 8 & 0xF
        reg2 = operand >> 4 & 0xF
        self.registers[reg1] = self.registers[reg1] | self.registers[reg2]

    def setVXToVXandVY(self, operand):
        reg1 = operand >> 8 & 0xF
        reg2 = operand >> 4 & 0xF
        self.registers[reg1] = self.registers[reg1] & self.registers[reg2]

    def setVXToVXxorVY(self, operand):
        reg1 = operand >> 8 & 0xF
        reg2 = operand >> 4 & 0xF
        self.registers[reg1] = self.registers[reg1] ^ self.registers[reg2]

    def addVYToVX(self, operand):
        reg1 = operand >> 8 & 0xF
        reg2 = operand >> 4 & 0xF
        sum = self.registers[reg1] + self.registers[reg2]
        if sum > 255:
            sum -= 255
            self.registers[0xF] = 1
        self.registers[reg1] = sum

    def subtractVYFromVX(self, operand):
        reg1 = operand >> 8 & 0xF
        reg2 = operand >> 4 & 0xF
        difference = self.registers[reg1] - self.registers[reg2]
        if difference < 0:
            difference += 255
            self.registers[0xF] = 1
        self.registers[reg1] = difference

    def subtractVXFromVYPlaceInVX(self, operand):
        reg1 = operand >> 8 & 0xF
        reg2 = operand >> 4 & 0xF
        difference = self.registers[reg2] - self.registers[reg1]
        if difference < 0:
            difference += 255
            self.registers[0xF] = 1
        self.registers[reg1] = difference

    def shiftVXRight(self, operand):
        reg1 = operand >> 8 & 0xF
        self.registers[0xF] = self.registers[reg1] & 0x0001
        self.registers[reg1] = self.registers[reg1] >> 1

    def shiftVXLeft(self, operand):
        reg1 = operand >> 8 & 0xF
        self.registers[0xF] = (self.registers[reg1] & 0x80) >> 7
        self.registers[reg1] = self.registers[reg1] << 1 & 0xFF

    def executeInstruction(self, opcode=None):
        if opcode:
            self.opcode = opcode
        else:
            self.opcode = self.memory[self.PC] << 8
            self.opcode += self.memory[self.PC + 1]
        self.PC += 2
        operation = (self.opcode & 0xF000) >> 12
        self.opcodes[operation](self.opcode)
