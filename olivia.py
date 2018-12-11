from prose_engine import PhraseDict
from data_format import parse, assemble
#           ------ Setup variables ------

statement = ""
mem = {
    'name':'',
    'gender':-1
    }

#           ------ Main loop ------

print("Hello there")

while True:
    statement = parse(input("=> "))
    if 'goodbye' in statement or statement == []: break
    print(assemble(statement))

print("Goodbye friend")
# Stops window from closing immediatly
input()
