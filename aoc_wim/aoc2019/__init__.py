import logging
from collections import defaultdict
from collections import deque


# logging.basicConfig(level=logging.INFO, format="    %(message)s")
log = logging.getLogger(__name__)

# "parameter modes"
POSITION = 0
IMMEDIATE = 1
RELATIVE = 2


class IntComputer:
    class Halt(Exception):
        pass

    def __init__(self, reg0, inputs=()):
        self.ip = 0
        if not isinstance(reg0, (list, tuple)):
            reg0 = [int(x) for x in reg0.split(",")]
        self.offset = 0
        self.reg = defaultdict(int, dict(enumerate(reg0)))
        self.input = deque(inputs)
        self.output = deque()
        self._iterations = 0
        self._last_instruction = None
        self.op_map = {
            1: self.op_add,
            2: self.op_mul,
            3: self.op_input,
            4: self.op_output,
            5: self.op_jump_t,
            6: self.op_jump_f,
            7: self.op_lt,
            8: self.op_eq,
            9: self.op_offset,
            99: self.op_halt,
        }

    def op_add(self, x, y, z):
        self.reg[z] = self.reg[x] + self.reg[y]

    def op_mul(self, x, y, z):
        self.reg[z] = self.reg[x] * self.reg[y]

    def op_input(self, x):
        self.reg[x] = self.input.pop()

    def op_output(self, x):
        self.output.appendleft(self.reg[x])

    def op_jump_t(self, x, y):
        if self.reg[x]:
            self.ip = self.reg[y] - 3

    def op_jump_f(self, x, y):
        if not self.reg[x]:
            self.ip = self.reg[y] - 3

    def op_lt(self, x, y, z):
        self.reg[z] = int(self.reg[x] < self.reg[y])

    def op_eq(self, x, y, z):
        self.reg[z] = int(self.reg[x] == self.reg[y])

    def op_offset(self, x):
        self.offset += self.reg[x]

    def op_halt(self):
        raise IntComputer.Halt

    def step(self):
        opcode = self.reg[self.ip]
        modes, opnum = divmod(opcode, 100)
        op = self.op_map[opnum]
        nargs = op.__func__.__code__.co_argcount - 1
        modes = [modes // (10 ** n) % 10 for n in range(nargs)]
        assert set(modes) <= {POSITION, IMMEDIATE, RELATIVE}
        args = []
        for i, mode in enumerate(modes, start=1):
            if mode == IMMEDIATE:
                args.append(self.ip + i)
            elif mode == POSITION:
                args.append(self.reg[self.ip + i])
            elif mode == RELATIVE:
                args.append(self.reg[self.ip + i] + self.offset)
        log.info(
            "%d processing ip=%-5d opcode=%-5d op=%-10s offset=%-5d modes=%-10s args=%s",
            self._iterations,
            self.ip,
            opcode,
            op.__name__,
            self.offset,
            modes,
            args,
        )
        self._last_instruction = op.__func__
        op(*args)
        self._iterations += 1
        self.ip += nargs + 1

    def run(self, until=None):
        while True:
            try:
                self.step()
            except IntComputer.Halt:
                break
            if self._last_instruction is until:
                break
