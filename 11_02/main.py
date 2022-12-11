
from dataclasses import dataclass
from functools import reduce
import re
from io import TextIOWrapper
import sys
from typing import List

def match_and_get(line: str, r: str) -> str:
    m = re.match(rf'^\s*{r}$', line)
    if not m:
        raise ValueError(f"Invalid input at '{line}'")
    return m.group(1)

@dataclass
class Thing:
    worry_level: int = 0

class Monkey:
    def __init__(self, id: int):
        self.id: int = id
        self.things: List[Thing] = []
        self.opeartion: str = ''
        self.inspection_count: int = 0

    def deserialize(self, input: TextIOWrapper):
        get_line = lambda: input.readline().strip()
        
        [self.things.append(Thing(int(i))) for i in match_and_get(get_line(), r'Starting items\: (.+)').split(',')]
        self.operation = match_and_get(get_line(), r'Operation\: new \= (.+)')
        self.div_test = int(match_and_get(get_line(), r'Test\: divisible by (.+)'))
        self.throw_monkeys = [
            int(match_and_get(get_line(), r'If true\: throw to monkey (.+)')),
            int(match_and_get(get_line(), r'If false\: throw to monkey (.+)'))
        ]

def step_monkey(monkeys: List[Monkey], index: int, common_div: int):
    monkey = monkeys[index]
    things_to_remove: List[Thing] = []
    for thing in monkey.things:
        monkey.inspection_count += 1
        thing.worry_level = int(eval(monkey.operation.replace('old', str(thing.worry_level)))) % common_div
        throw_index = 0 if thing.worry_level % monkey.div_test == 0 else 1
        monkeys[monkey.throw_monkeys[throw_index]].things.append(thing)
        things_to_remove.append(thing)
    monkey.things = [thing for thing in monkey.things if thing not in things_to_remove]

def play_round(monkeys: List[Monkey], common_div: int):
    for i in range(len(monkeys)):
        step_monkey(monkeys, i, common_div)

def get_monkey_bussiness(monkeys: List[Monkey]) -> int:
    ordered: List[Monkey] = sorted(monkeys, key=lambda m:m.inspection_count, reverse=True)
    return ordered[0].inspection_count * ordered[1].inspection_count

monkeys: List[Monkey] = []

with open('input.txt', 'r') as input:
    while True:
        try:
            id = int(match_and_get(input.readline().strip(), r'Monkey (\d+)\:'))
        except ValueError:
            break
        monkey = Monkey(id)
        monkey.deserialize(input)
        monkeys.append(monkey)
        input.readline()

# Use a common_div as a way to reduce the worry to a sane level common for all monkeys
unique_divs = set(m.div_test for m in monkeys)
common_div: int = reduce(lambda a,b:a*b, unique_divs, 1)

for _ in range(10000):
    play_round(monkeys, common_div)

print(get_monkey_bussiness(monkeys))