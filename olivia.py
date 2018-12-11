from prose_engine import PhraseDict

# ------ Define functions and classes ------
    
def parse(val):
    '''Takes a string and splits it into an array of words'''
    val = str(val)
    wordList = val.lower().split()
    for i in range(len(wordList)):
        if i >= len(wordList): break
        wordList[i] = wordList[i].strip('.,()!?~ ')
        if wordList[i] == '': del wordList[i]
    return wordList    

def assemble(val):
    '''Takes an array of individual strings and combines into a sentence'''
    out = ''
    for i in val:
        out += i + ' '
    return out.strip().capitalize()
        
# ------ Setup variables ------

statement = ""
mem = {
    'name':'',
    'gender':-1
    }

# ------ Main loop ------

print("Hello there")

while True:
    statement = parse(input("=> "))
    if 'goodbye' in statement or statement == []: break
    print(assemble(statement))
print("Goodbye friend")
# Stops window from closing immediatly
input()
