import unittest
from chip8 import chip8
"""
    Testklass for Chip8 instruktionerna.
    Instruktioner for alla OP-koderna kan hittas har:
    https://en.wikipedia.org/wiki/CHIP-8#Opcode_table
"""


class chip8_test(unittest.TestCase):
    # 1NNN
    def testInstructionJumpTo(self):
        cpu = chip8()
        cpu.PC = 0
        cpu.executeInstruction(0x1FFF)
        self.assertEqual(cpu.PC, 0x0FFF)

    # 3XNN
    def testInstructionSkipsTheNextInstructionIfVXEqualsNN(self):
        cpu = chip8()
        cpu.PC = 0
        cpu.registers[0xA] = 0xFF
        self.assertEqual(cpu.registers[0xA], 0xFF)
        self.assertEqual(cpu.PC, 0)
        cpu.executeInstruction(0x3AFF)
        self.assertEqual(cpu.PC, 4)
        cpu.executeInstruction(0x3AFA)
        self.assertEqual(cpu.PC, 6)

    # 4XNN
    def testInstructionSkipsTheNextInstructionIfVXDoesNotEqualsNN(self):
        cpu = chip8()
        cpu.PC = 0
        cpu.registers[0xA] = 0xFF
        self.assertEqual(cpu.registers[0xA], 0xFF)
        self.assertEqual(cpu.PC, 0)
        cpu.executeInstruction(0x4AFF)
        self.assertEqual(cpu.PC, 2)
        cpu.executeInstruction(0x4AFA)
        self.assertEqual(cpu.PC, 6)

    # 5XY0
    def testSkipNextInstructionIfVXEqualsVY(self):
        cpu = chip8()
        cpu.PC = 0
        cpu.registers[0xA] = 0xFF
        self.assertEqual(cpu.registers[0xA], 0xFF)
        self.assertEqual(cpu.PC, 0)
        cpu.executeInstruction(0x5AF0)
        self.assertEqual(cpu.PC, 2)
        cpu.registers[0xF] = 0xFF
        self.assertEqual(cpu.registers[0xF], 0xFF)
        cpu.executeInstruction(0x5AF0)
        self.assertEqual(cpu.PC, 6)

    # 6XNN
    def testSetValueToVX(self):
        cpu = chip8()
        cpu.registers[0xA] = 0x0
        self.assertEqual(cpu.registers[0xA], 0x0)
        cpu.executeInstruction(0x6AFA)
        self.assertEqual(cpu.registers[0xA], 0xFA)

    # 7XNN
    def testAddValueToVX(self):
        cpu = chip8()
        cpu.registers[0xA] = 0x5
        self.assertEqual(cpu.registers[0xA], 0x5)
        cpu.executeInstruction(0x7A05)
        self.assertEqual(cpu.registers[0xA], 0xA)

    # 8XY0
    def testSetVXToVY(self):
        cpu = chip8()
        cpu.registers[0xA] = 0x0
        cpu.registers[0xF] = 0xFA
        self.assertEqual(cpu.registers[0xA], 0x0)
        cpu.executeInstruction(0x8AF0)
        self.assertEqual(cpu.registers[0xA], 0xFA)

    # 8XY1
    def testSetVXToVXorVY(self):
        cpu = chip8()
        cpu.registers[0xA] = 0xC
        cpu.registers[0xF] = 0x3
        cpu.executeInstruction(0x8AF1)
        self.assertEqual(cpu.registers[0xA], 0xF)

    # 8XY2
    def testSetVXToVXandVY(self):
        cpu = chip8()
        cpu.registers[0xA] = 0x7
        cpu.registers[0xF] = 0x3
        cpu.executeInstruction(0x8AF2)
        self.assertEqual(cpu.registers[0xA], 0x3)

    # 8XY3
    def testSetVXToVXxorVY(self):
        cpu = chip8()
        cpu.registers[0xA] = 0x2
        cpu.registers[0xF] = 0xA
        cpu.executeInstruction(0x8AF3)
        self.assertEqual(cpu.registers[0xA], 0x8)

    # 8XY4
    def testAddVYToVXWithCarry(self):
        cpu = chip8()
        cpu.registers[0xA] = 0xFF
        cpu.registers[0xE] = 0xFA
        cpu.executeInstruction(0x8AE4)
        self.assertEqual(cpu.registers[0xA], 0xFA)
        self.assertEqual(cpu.registers[0xF], 0x1)

    # 8XY5
    def testSubtractVYFromVYWithCarry(self):
        cpu = chip8()
        cpu.registers[0xA] = 0xA
        cpu.registers[0xE] = 0xF
        cpu.executeInstruction(0x8AE5)
        self.assertEqual(cpu.registers[0xA], 0xFA)
        self.assertEqual(cpu.registers[0xF], 0x1)

    # 8XY6
    def testShiftVXRight(self):
        cpu = chip8()
        cpu.registers[0xA] = 0x3
        cpu.executeInstruction(0x8AE6)
        self.assertEqual(cpu.registers[0xA], 0x1)
        self.assertEqual(cpu.registers[0xF], 0x1)

        cpu.registers[0xA] = 0x2
        cpu.executeInstruction(0x8AE6)
        self.assertEqual(cpu.registers[0xA], 0x1)
        self.assertEqual(cpu.registers[0xF], 0x0)

    # 8XY7
    def testSetVXToSubtractionOfVXFromVYWithCarry(self):
        cpu = chip8()
        cpu.registers[0xA] = 0xF
        cpu.registers[0xE] = 0xA
        cpu.executeInstruction(0x8AE7)
        self.assertEqual(cpu.registers[0xA], 0xFA)
        self.assertEqual(cpu.registers[0xF], 0x1)

    # 8XYE
    def testShiftVXLeft(self):
        cpu = chip8()
        cpu.registers[0xA] = 0x8A
        cpu.executeInstruction(0x8AEE)
        self.assertEqual(cpu.registers[0xA], 0x14)
        self.assertEqual(cpu.registers[0xF], 0x1)

        cpu.registers[0xA] = 0x2
        cpu.executeInstruction(0x8AEE)
        self.assertEqual(cpu.registers[0xA], 0x4)
        self.assertEqual(cpu.registers[0xF], 0x0)


if __name__ == '__main__':
    unittest.main()
