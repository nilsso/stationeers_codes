belt_hash = -676435305
ore_hashes = [ 1724793494, -707307845, 1758427767, -1348105509, -916518678, -190236170, 1103972403,
        1830218956, -983091249, -1516581844, 1217489948, -1805394113, 1253102035]

q = 15

# print(belt_hash % q)
# print(not any(belt_hash % q == h % q for h in ore_hashes))
for h in ore_hashes:
    print(h % q)
    # for x in range(2, 15):
        # if (h % q) % x == 0:
            # print(x)
            # break

from functools import reduce

m = reduce(lambda x, y: x * (y % q), ore_hashes)
print(m)

print(m % (belt_hash % q))
for h in ore_hashes:
    print(m % (h % q))

