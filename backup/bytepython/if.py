number = 23
guess = int(input("Enter an integer:"))

if guess == number:
    print("equal")
elif guess < number:
    print("less than")
else:
    print("great or equal than")

print("done")
