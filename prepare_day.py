
import os
from pathlib import Path
import sys
import requests
import markdownify
from bs4 import BeautifulSoup

# requires
# - bs4
# - markdownify

if len(sys.argv) == 1:
    print ('prepare_day yyyy/dd 1|2')
    print ('Remember to set your session cookie in AOC_SESSION')
    sys.exit(0)

# Quick .env management
env = dict(line.strip().split('=', maxsplit=1) for line in open('.env', 'r').readlines())

SESSION = env.get('AOC_SESSION', os.environ.get('AOC_SESSION', None))
if not SESSION:
    raise Exception('Missing AOC_SESSION environment variable')

year, day = sys.argv[1].split('/', maxsplit=1)

dir_name = '%02d' % int(day)

try:
    part = int(sys.argv[2])
except:
    part = 1

if part != 1:
    dir_name += '_%02d' % part

if Path.is_dir(Path(dir_name)):
    raise Exception(f'Directory {dir_name} already exists')

headers = { 'cookie': f'session={SESSION}' }
page = requests.get(f"https://adventofcode.com/{year}/day/{day}", headers=headers)
input = requests.get(f"https://adventofcode.com/{year}/day/{day}/input", headers=headers)

soup = BeautifulSoup(page.content, 'html.parser')
text = soup.find_all('article')[part - 1]
md = markdownify.markdownify(str(text), heading_style="ATX")

os.mkdir(dir_name)
with open(f'{dir_name}/input.txt', 'w') as f:
    f.write(input.content.decode())

with open(f'{dir_name}/README.md', 'w') as f:
    f.write(md)
