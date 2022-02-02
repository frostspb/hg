import math


def y(x):
    return x**3 + math.cos(x)**4


i = -2.0
res_list = []

while i <= 2.0:
    val = y(i)
    if val > 0:
        res_list.append(val)
    i += 0.5

print(res_list)

result = sum(res_list) / len(res_list)

print(f"Average = {result}")
