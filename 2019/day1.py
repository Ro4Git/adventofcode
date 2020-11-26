

def compute_fuel(in_value):
    fuel_needed = int(in_value / 3) - 2
    if (fuel_needed < 0):
        return 0
    return fuel_needed + compute_fuel(fuel_needed)
    

f = open('input_day1.txt','r')
lines = f.readlines()
f.close()

sum = 0

for line in lines:
    value = int(line)
    result = compute_fuel(value)
    sum = sum + result
    print(sum)


