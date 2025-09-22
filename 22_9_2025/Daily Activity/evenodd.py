def check(n):
    if n % 2 == 0:
        return f"{n} is even"
    else:
        return f"{n} is odd"

n = int(input("Enter no: "))
print(check(n))