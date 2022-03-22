a = (1,11)
b = (2,22)
c = (3,33)

print(list(zip(a,b,c)))

for x in zip(a,b,c):
    print(x, end=" ")