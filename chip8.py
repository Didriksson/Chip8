class chip8(object):
    def __init__(self):
        # As per chip8 specs PC starts per default at address 512.
        self.PC = 0x200
        self.I = bytearray(2)

        self.registers = bytearray(16)

        self.memory = bytearray(4096)
        self.opcodes = {
            0x1: self.jumpToAddress,
            0x3: self.skipNextInstructionIfVXEqualsNN
        }

    def jumpToAddress(self, operand):
        self.PC = operand & 0x0FFF

    def skipNextInstructionIfVXEqualsNN(self, operand):
        pass
    def executeInstruction(self, opcode=None):
        if opcode:
            self.opcode = opcode
        else:
            self.opcode = self.memory[self.PC] << 8
            self.opcode += self.memory[self.PC + 1]
            self.PC += 2
        operation = (self.opcode & 0xF000) >> 12
        self.opcodes[operation](self.opcode)
