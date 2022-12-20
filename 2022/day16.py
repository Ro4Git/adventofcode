#Advent of code 2022: Day 16
#https://adventofcode.com/2022/day/16
import re, time, copy

f = open('input_day16.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

lines = [re.split('[\\s=;,]+', line) for line in lines]
valves = {item[1]: set(item[10:]) for item in lines}
flows = {item[1]: int(item[5]) for item in lines if int(item[5]) > 0}
masks = {x: 1<<i for i, x in enumerate(flows)}
timeCosts = {x: {y: 1 if y in valves[x] else float('+inf') for y in valves} for x in valves}
for k in timeCosts:
    for i in timeCosts:
        for j in timeCosts:
            timeCosts[i][j] = min(timeCosts[i][j], timeCosts[i][k]+timeCosts[k][j])

def visit(valve, remainingTime, state, flow, answer):
    answer[state] = max(answer.get(state, 0), flow)
    for nextValve in flows:
        nextRemainingTime = remainingTime - timeCosts[valve][nextValve] - 1
        if (masks[nextValve] & state) or (nextRemainingTime <= 0):
             continue
        visit(nextValve, nextRemainingTime, state | masks[nextValve], flow + nextRemainingTime * flows[nextValve], answer)
    return answer    


def part1():
    visits = visit('AA', 30, 0, 0, {})
    print(len(visits.values()))
    total = max(visits.values())
    print(total)

def part2():
    visits = visit('AA', 26, 0, 0, {})
    print(len(visits.values()))
    total = max(v1+v2 for k1, v1 in visits.items() 
                    for k2, v2 in visits.items() if not k1 & k2)
    print(total)


print("----- Part1 ----")
startp1 = time.time()
part1()
endp1 = time.time()
print("{:.4f}s".format(endp1 - startp1))

print("----- Part2 ----")
startp2 = time.time()
part2()
endp2 = time.time()
print("{:.4f}s".format(endp2 - startp2))