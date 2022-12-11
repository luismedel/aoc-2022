
from dataclasses import dataclass
import re
from io import TextIOWrapper
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

def step_monkey(monkeys: List[Monkey], index: int):
    monkey = monkeys[index]
    things_to_remove: List[Thing] = []
    for thing in monkey.things:
        monkey.inspection_count += 1
        thing.worry_level = int(eval(monkey.operation.replace('old', str(thing.worry_level)))) // 3
        throw_index = 0 if thing.worry_level % monkey.div_test == 0 else 1
        monkeys[monkey.throw_monkeys[throw_index]].things.append(thing)
        things_to_remove.append(thing)
    monkey.things = [thing for thing in monkey.things if thing not in things_to_remove]

def play_round(monkeys: List[Monkey]):
    for i in range(len(monkeys)):
        step_monkey(monkeys, i)

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

for _ in range(20):
    play_round(monkeys)

print(get_monkey_bussiness(monkeys))