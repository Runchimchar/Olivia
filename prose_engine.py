from stack_array import Stack

class WordNode:
    '''A single word within a phrase, to be followed by more words
        May contain a special string/object to define it as a special word'''

    def __init__(self, word):
        '''Assign word and handle special strings'''
        if word == "None":
            self.word = None
        else:
            self.word = word
        self.children = []

    def __repr__(self):
        '''Recursivly print contained word and children (if any)'''
        if self.children == []:
            childStr = ''
        else: 
            childStr = "" + str(self.children)
        return str(self.word) + "" + childStr

class PhraseDict:
    '''A tree of words that is explored to find ideas'''
    def __init__(self,source):
        self.source = source
        self.root = WordNode(None)
        self.__build__(source)

    def __str__(self):
        return str(self.root)

    def __build__(self,source):
        '''takes a properly formatted phrase file and builds the tree'''
        with open(source,'r') as f:
            text = f.read().split('\n')
        wordStack = Stack(15)
        depth = 0
        currWord = self.root
        last = None
        for i in range(len(text)):
            #print(text[i])
            tCount = text[i].count('\t')
            # If tab depth increases
            if tCount > depth:
                wordStack.push(currWord)
                depth += 1
                currWord = last
            # If tab depth decreases
            while tCount < depth:
                depth -= 1
                currWord = wordStack.pop()
            # After the depth is adjusted, add the word to the tree
            last = WordNode(text[i].strip())
            currWord.children += [last]


# ------- DEBUG TESTING -------
if __name__ == "__main__":   
    p = PhraseDict('phrases1.txt')
    print(p)
