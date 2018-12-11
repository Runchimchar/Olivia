from prose_engine import PhraseDict, WordDict
from data_format import * 

looping = True
class Chatterbot:
    '''Tester chatbot with primitive inteligence systems'''
    def __init__(self):
        self.awake = False
        self.pd = PhraseDict('assets/phrases.txt')
        self.wd = WordDict('assets/words.txt')

    def __decode(self,code, words):
        if code == -1:
            print('~-~\nwhat?')
        elif code == 0:
            print("OuO\nHello "+words[0]+", my name's Chatterbot.")
        elif code == 1:
            print('oWo\nHi '+words[0]+', I\'m Chatterbot!')
        elif code == 2:
            print('O.O\nWell I\'m a '+words[0]+' chatbot.')
        elif code == 4:
            print("O~O\nI'm not very smart yet, so I'll assume being "+words[0]+" is a good thing.")
        elif code == 5:
            print("T^T\nAww, bye then.")
            self.sleep()

    def start(self):
        self.awake = True
        while self.awake:
            code, words = self.pd.explore(parse(input("> "),self.wd))
            self.__decode(code, words)

    def sleep(self):
        self.awake = False

#           ------ Main runner ------

def main():
    bot = Chatterbot()
    bot.start()

if __name__ == "__main__":
    main()
