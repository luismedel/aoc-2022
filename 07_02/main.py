from dataclasses import dataclass
import re

input = open ('input.txt', 'r')

@dataclass
class Entry:
    def __init__(self, name, size=-1):
        self.name = name
        self.parent = None
        self.size = size
    
    def get_size(self):
        return self.size
    
    def __str__(self):
        return self.name

@dataclass
class File(Entry):
    def __init__(self, name, size):
        super().__init__(name, size)

@dataclass
class Dir(Entry):
    def __init__(self, name):
        super().__init__(name)
        self.entries = { '.': self }
    
    def add_entry(self, entry, key=None):
        self.size = -1

        entry.parent = self
        if isinstance(entry, Dir):
            entry.entries['..'] = self

        self.entries[key or entry.name] = entry

    def valid_entries(self):
        return (v for k, v in self.entries.items() if not k.startswith('.'))

    def get_size(self):
        if self.size == -1:
            self.size = sum(e.get_size() for e in self.valid_entries())
        return self.size

    def get_full_path(self):
        return (f'{self.parent.get_full_path() if self.parent else ""}/{self.name}')

def parse_file(line):
    match = re.match(r'^(\d+) (.+)$', line)
    if not match:
        return None
    return File(match.group(2), int(match.group(1)))

def parse_dir(line):
    match = re.match(r'^dir (.+)$', line)
    if not match:
        return None
    return Dir(match.group(1))

def filter_dirs(dir, min_size, results):
    for e in dir.valid_entries():
        if isinstance(e, Dir):
            filter_dirs(e, min_size, results)
    if dir.get_size() >= min_size:
        results.append(dir)

def print_dir(dir, padding=''):
    files = (v for k, v in dir.entries.items() if not k.startswith('.') and isinstance(v, File))
    dirs = (v for k, v in dir.entries.items() if not k.startswith('.') and isinstance(v, Dir))

    for e in files:
        print(f'{padding}{e.size}\t{e.name}')

    for e in dirs:
        print(f'{padding}{e.name}/')
        print_dir(e, padding + '  ')

root = Dir('/')
current_dir = root

lines = input.readlines()
i = 0
while i < len(lines):
    line = lines[i].rstrip()
    i += 1
    match = re.match(r'^\$ cd (.+)$', line)
    if match:
        d = match.group(1)
        if d == '/':
            current_dir = root
        else:
            current_dir = current_dir.entries[d]
        continue

    match = re.match(r'^\$ ls', line)
    if match:
        while (i < len(lines)):
            line = lines[i].rstrip()
            i += 1

            if line.startswith('$'):
                i -= 1
                break

            entry = parse_file(line) or parse_dir(line)
            current_dir.add_entry(entry)
        continue

free = 70000000 - root.get_size()
needed = 30000000 - free

results = []
filter_dirs(root, needed, results)
results.sort(key=lambda d: d.get_size())
print(results[0].get_size())