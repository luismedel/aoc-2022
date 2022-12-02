
EQUIV = { 'A':'X', 'B':'Y', 'C':'Z' }
RPS = { 'X':(1,'C'), 'Y':(2,'A'), 'Z':(3,'B') }

total_score = 0

with open('input.txt', 'r') as input:
    for s in input:
        round_moves = s.rstrip().split(' ')
        score = RPS[round_moves[1]]
        total_score += score[0]

        # Draw
        if EQUIV.get(round_moves[0], '') == round_moves[1]:
            total_score += 3

        # Win
        if round_moves[0] == score[1]:
            total_score += 6

print(total_score)
