from structures import Stack
from enum import Enum

class WordNode:
        '''A single word within a phrase, to be followed by more words
                May contain a special string/object to define it as a special word'''

        def __init__(self, word):
                '''Assign word and handle special strings'''
                self.word = word
                self.children = []
                self.code = None

        def __repr__(self):
                '''Recursivly return contained word and children (if any)'''
                if self.children == []:
                        childStr = ''
                else: 
                        childStr = "" + str(self.children)
                return str(self.word) + "" + childStr

        def __str__(self):
                '''Return the word'''
                return str(self.word)

        def __eq__(self,other):
                if type(other) is WordNode:
                        return self.word == other.word
                elif type(other) is str:
                        return self.word == other
                else:
                        return False

        def get_child(self,wordStr):
                '''Return the child matching wordStr or a None node if there are no matches and one exists'''
                noneNode = None
                for c in self.children: 
                        if c.word == wordStr: return c
                        if c == "BLANK": noneNode = c
                return noneNode


class PhraseDict:
        '''A tree of words that is explored to find ideas'''
        def __init__(self,source):
                self.source = source
                self.root = WordNode(None)
                self.__build__(source)

        def __str__(self):
                return repr(self.root)

        def __build__(self,source):
                '''takes a properly formatted phrase file and builds the tree'''
                with open(source,'r') as f:
                        lines = f.read().split('\n')
                
                wordStack = Stack(len(lines)//2)
                depth = 0
                currWord = self.root
                last = None

                # Add create and children to WordNodes
                for i in range(len(lines)):
                        #print(lines[i])
                        # Ignore comments
                        if lines[i].strip().startswith('#'):
                                continue
                        if lines[i].find('#') != -1:
                                lines[i] = lines[i].partition('#')[0].rstrip()
                        tCount = lines[i].count('\t')
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
                        last = WordNode(lines[i].strip())
                        currWord.children += [last]
                
                # Add codes to leaves
                self.__add_codes_rec__(self.root)
                
        def __add_codes_rec__(self,node,code=0):
                '''Recursively find leaves below node and give them a code based on the order their found'''
                if node.children == []:
                        node.code = code
                        #print(str(node)+', '+str(code))
                        return code+1
                else:
                        for child in node.children:
                                code = self.__add_codes_rec__(child,code)
                        return code

        def explore(self,wordList):
                '''Takes a list of formated words and explores the tree'''
                inputWords = []
                blankWord = []
                endCode = -1

                currWord = self.root
                for word in wordList:
                        child = currWord.get_child(word)
                        # if no match, reset to root
                        if child is None:
                                if currWord == "BLANK":
                                        blankWord.append(word)
                                else:
                                        currWord = self.root
                        # if matching word is found
                        else:
                                # if entering a BLANK space
                                if child == "BLANK":
                                        blankWord.append(word)
                                # if exiting a BLANK space
                                if currWord == "BLANK":
                                        inputWords.append(' '.join(blankWord))
                                        blankWord = []
                                # No matter what, if a match is found, update currWord
                                currWord = child
                        # if end of phrase reached
                        if currWord.children == []:
                                endCode = currWord.code
                
                # if a match was never found, the inputted words wont be added right
                if blankWord != []: inputWords.append(' '.join(blankWord))

                return endCode, inputWords


class Definition:
        '''A word and words related to it'''
        def __init__(self):
                pass
                
class WordDict:
        '''A dictionary of learned words'''
        def __init__(self,commonFile,synonymFile):
                # Handle common words file
                wordFile = open(commonFile,'r')
                self.commonWords = wordFile.read().split()
                wordFile.close()

                # Handle synonyms file
                self.synList = []
                synFile = open(synonymFile,'r')
                for line in synFile:
                        self.synList.append([])
                        self.synList[-1] = line.strip().split(', ')
                synFile.close()
                
                self.wordDict = {}
        
        def check_word(self, word):
                '''See if a given word is a common word and should be uncapitalized'''
                return word in self.commonWords
                
        def simplify(self, data):
                '''Translate a given word into a more understood form'''
                if type(data) is str:
                        for syns in self.synList:
                                if data in syns:
                                        return syns[0]
                        return data
                elif type(data) is list:
                        for i in range(len(data)):
                                data[i] = self.simplify(data[i])
                        return data
                else:
                        return None
                                

class Emote:
        def __init__(self, facepath):
                self.faceData = []
                self.loadFaces(facepath)

        def loadFaces(self, facepath):
                '''Load faces into faceData from a file'''
                file = None
                reading = False
                try:
                        file = open(facepath)
                except:
                        print("Error: file \""+facepath+"\" not found")
                        return None
                for line in file:
                        if line.strip() == "#BEGINLIST":
                                reading = True
                        elif line.strip() == "#ENDLIST":
                                reading = False
                        elif reading:
                                text = line.split("\t")
                                self.faceData.append((text[0],float(text[1]),float(text[2])))
        
        def getFaces(self):
                return self.faceData
        

# ------- DEBUG TESTING -------
if __name__ == "__main__":   
        p = PhraseDict('assets/phrases.txt')
        print(p.explore(['my','name','is','Jenna','Whilden']))
        e = Emote('assets/faces.txt')
        for face in e.getFaces():
                print(face)
        #print(p)
