
EQUIV = { 'A':'X', 'B':'Y', 'C':'Z' }
RPS = { 'A':(1,'C'), 'B':(2,'A'), 'C':(3,'B') }

total_score = 0

with open('input.txt', 'r') as input:
    for s in input:
        round_moves = s.rstrip().split(' ')

        next_move = ''
        if round_moves[1] == 'X':
            next_move = RPS[round_moves[0]][1]
        elif round_moves[1] == 'Y':
            next_move = round_moves[0]
            total_score += 3
        else:
            next_move = next((k for k, v in RPS.items() if v[1] == round_moves[0]), None)
            total_score += 6
        print(round_moves[0], next_move)
        total_score += RPS[next_move][0]

print(total_score)
