print("Hello there")
statement = ""
while True:
    statement = input("=> ")
    if statement.lower().find("goodbye") == 0: break
    print(statement)
print("Goodbye friend")
input()
