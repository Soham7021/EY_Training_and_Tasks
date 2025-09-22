# for i in range(1,6):
#     print(i)

def table(n):
    print(f"multiplication table for {n}")
    for i in range(1,11):
        print(f"{n} * {i} = {n * i}")

n = int(input("Enter no: "))
table(n)