
from collections import namedtuple
from enum import Enum
from typing import Dict, Iterable, Tuple

class Opcode(Enum):
    NOOP = 0,
    ADDX = 1,
    HALT = 99

CYCLES = {
    Opcode.NOOP: 1,
    Opcode.ADDX: 2,
    Opcode.HALT: 0,
}

Mnemonic = namedtuple('Mnemonic', ('opcode', 'argc'))

MNEMONICS = {
    'noop': Mnemonic(Opcode.NOOP, 0),
    'addx': Mnemonic(Opcode.ADDX, 1),
}

Instr = namedtuple('Instr', ('op', 'args'))


class VM:
    def __init__(self, program: Iterable[Instr]):
        self.regs: Dict[str, int] = {
            'X': 1,
        }
        self.program: Tuple[Instr] = tuple(program) + (Instr(Opcode.HALT, None), )
        self.cycle: int = 0
        self.pc: int = 0
        self._wait: int = -1
        self._instr: Instr = None
        self.reset()

    def reset(self):
        self.regs.update({
            'X': 1,
        })
        self.cycle = 0
        self.pc = 0
        self._wait = -1
        self._instr = None
        self.fetch()

    def fetch(self):
        self._instr = self.program[self.pc]
        self._wait = CYCLES[self._instr.op]
        self.pc += 1

    def step(self) -> bool:
        if self._wait == 0:
            instr = self._instr
            if instr.op == Opcode.NOOP:
                pass
            elif instr.op == Opcode.ADDX:
                self.regs['X'] += int(instr.args[0])
            self.fetch()

            if self._instr.op == Opcode.HALT:
                return False

        self.cycle += 1
        self._wait -= 1
        return True

    @property
    def signal_strength(self) -> int:
        return self.cycle * self.regs['X']

def parse_op(line: str) -> Instr:
    parts = line.split(' ', maxsplit=1)
    if parts[0] not in MNEMONICS:
        raise ValueError(f"Unknown mnemonic '{parts[0]}'")
    m = MNEMONICS[parts[0]]
    if (m.argc == 0):
        return Instr(m.opcode, None)
    args = parts[1].split(',')  # Let's imagine we use comma to separate args
    return Instr(m.opcode, tuple(args[:m.argc]))

program = (parse_op(line.rstrip()) for line in open('input.txt', 'r'))

cycles = (20, 60, 100, 140, 180, 220)

vm = VM(program)

strengths = []
for c in cycles:
    vm.reset()
    for i in range(c):
        vm.step()
    strengths.append(vm.signal_strength)

print(sum(strengths))
