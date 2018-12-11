from sys import argv
import os

#           ------ File formater class ------

class Formater(object):
	'''Takes a file and formats it's contents'''
	def __init__(self, filename, argDict = {}):
		self.filename = filename
		#print(str(argDict))
		self._seperator = (argDict['-s'] if '-s' in argDict else None)
		#print(str(self._seperator))
		self.contents = []
		self.payload = []
		
	def __str__(self):
		#outStr = ''
		#for line in self.contents:
			#for data in line:
			#	outStr += data + ', '
			#outStr += str(line) + '\n'
		linesList = []
		for line in self.contents:
			linesList.append(', '.join(line))
		
		return '\n'.join(linesList)
			
	def format2D(self):
		'''Format the given file by splitting up lines by the given seperator'''
		file = self.__openFile()
		if file is None: return -1
		
		self.contents = []
		
		for line in file:
			if self._seperator is None:
				dataList = line.strip().split()
			else:
				dataList = line.strip().split(self._seperator)
			self.contents.append(dataList)
			self.payload.append(dataList[-1])
		
		file.close()
		return 0
		
	def __openFile(self, filename=None):
		if filename is None: filename = self.filename
		try:
			f = open(filename,'r')
		except FileNotFoundError as e:
			print('Error: File',filename,'is missing.')
			return None
		return f

#           ------ Various formating methods ------

def parse(val,wordDict=None):
    '''Takes a string and splits it into an array of words'''
    val = str(val)
    wordList = val.split()
    # use while rather than for because the length of wordList can both lengthen and shorten
    i = 0
    while i < len(wordList):
        wordList[i] = wordList[i].strip('.,()!?~ \t\n')
        if wordDict is not None and wordDict.check_word(wordList[i].lower()):
            wordList[i] = wordList[i].lower()
        if wordList[i].lower() == "i'm":
            wordList[i] = 'i'
            wordList.insert(i+1,'am')
        if wordList[i] == '': del wordList[i]
        # increment i
        i += 1
    return wordList

def assemble(val):
    '''Takes an array of individual strings and combines into a sentence'''
    out = ''
    for i in val:
        out += i + ' '
    return out.strip().capitalize()
		
#           ------ TESTER CODE ------

def main():
	'''Console line handler'''
	if len(argv) < 2 or len(argv) % 2 != 0:
		print("Usage: python3 data_format.py <filename> [tag arg]")
		return -1
	try:
		f = open(argv[1], 'r')
		f.close()
	except FileNotFoundError as e:
		print(argv[1], 'could not be found or opened')
		return -1
	
	formatDict = {}
	
	for i in range(1,(len(argv))//2):
		formatDict[argv[i*2]] = argv[i*2+1]
		
	formater = Formater(argv[1],formatDict)
	
def debug():
	'''DO STUFF TO TEST FUNCTIONALITY'''
	print('"dab on \'em"')
	
	path = os.path.dirname(os.path.abspath(__file__))
	formater = Formater(path+'\\movie-dialog-corpus\\movie_lines.txt', {'-s':' +++$+++ '})
	print(formater.format2D())
	#print(formater)
	for data in formater.payload:
		print(data)
	
if __name__ == '__main__': 
	#main()
	debug()
	#input()
