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
        cpu.executeInstruction(0x30FF)
        self.assertEqual(cpu.PC, 4)

if __name__ == '__main__':
    unittest.main()
