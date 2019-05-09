import tkinter as tk
from PIL import Image, ImageTk
import sys
import math


def err(text): sys.stderr.write(text+"\n")

class CanvasConsole(tk.Frame):
    def __init__(self, root, bdCol = "#000010", textBg = "BLACK", textFg = "WHITE",
                 consoleFont = ("Consolas",14), screenBg = "#003300",
                 screenFg = "#00ff00", screenW = 800, screenH = 400):
        super().__init__(root, bg=bdCol)
        self.shapeList = []

        if screenH < 200:
            screenH = 200
        if screenW < 200:
            screenW = 300
        
        # ------ START SCREEN -------

        sFrame = tk.Frame(self, bd=5, relief=tk.RIDGE, bg=bdCol)
        sFrame.pack(side=tk.TOP, expand=True, fill="x")

        screen = tk.Canvas(sFrame, height=screenH+1, width=screenW+1, bg=screenBg,
                           highlightthickness=0)
##        screen.create_oval(0+20,0+20,screenW-20,screenH-20, outline=screenFg)
        screen.pack(expand=True, fill="x")
        self.screen = screen #SAVE SCREEN

        # ------ END SCREEN -------

        # ------ START CONSOLE ------

        console = tk.Frame(self)
        console.pack(side=tk.BOTTOM, fill="x")

        # -------- START TEXTBOX --------

        textbox = tk.Frame(console, bd=5, relief=tk.RIDGE, bg=bdCol)
        textbox.pack(side=tk.LEFT, expand=True, fill="x")

        carrot = tk.Label(textbox, text=">", bg=textBg, fg=textFg, font=consoleFont,
                          bd=2, relief=tk.FLAT)
        carrot.pack(side=tk.LEFT, fill="none")

        textLine = tk.Entry(textbox, bg=textBg, fg=textFg, font=consoleFont,
                          insertbackground=textFg, insertwidth=1, bd=2, relief=tk.FLAT,
                          selectbackground="WHITE", selectforeground="BLACK")
        textLine.pack(side=tk.LEFT, expand=True, fill="both")
        textLine.focus()
        self.textLine = textLine #SAVE TEXTLINE

        consoleManager = ConsoleManager(textLine, screen, self)

        # -------- END TEXTBOX --------

        submitBtn = tk.Button(console, text="SUBMIT", font=("Consolas",11),
                              bd=3, width=8, bg="#222222", fg="WHITE",
                              activebackground="#333333", activeforeground="#dddddd")
        submitBtn.pack(side=tk.RIGHT, fill="y")
        submitBtn.config(command=consoleManager.func)
        self.submitBtn = submitBtn #SAVE SUBMITBTN

        # ------ END CONSOLE ------

        self.opDict = {
            "bdCol": bdCol,
            "textBg": textBg,
            "textFg": textFg,
            "consoleFont": consoleFont,
            "screenBg": screenBg,
            "screenFg": screenFg,
            "screenW": screenW,
            "screenH": screenH
        }

    def drawShape(self, shape):
        if type(shape) == type(()):
            if shape[0].lower() == "oval":
                index = self.screen.create_oval(shape[1],shape[2],shape[3],
                                   shape[4], outline=self.opDict["screenFg"])
                self.shapeList.append((index,shape[0].lower()))
            elif shape[0].lower() == "text":
                index = self.screen.create_text(shape[1],shape[2],text=shape[3],
                                    fill=self.opDict["screenFg"], anchor="nw", font=("Consolas",10))
                self.shapeList.append((index,shape[0].lower()))
            else:
                err("Error: shape style \""+shape[0]+"\" not found")
                return -1
            print("ADD -> "+str(self.shapeList))
            return index
        else:
            err("Error: drawShape takes a touple of arguments")

    def clearShape(self, shapeId):
        found = False
        for shape in self.shapeList:
            if shape[0] == shapeId:
                self.screen.delete(shapeId)
                self.shapeList.remove(shape)
                found = True
                break
        if not found:
            err("Err: Index not found")
        else:
            print("DEL -> "+str(self.shapeList))

    def config(self, name, value=None):
        if type(name) == type({}):
            # Process dictionaries
            for data in name.items():
                self.config(data[0], data[1])
            return
        if type(name) != str:
            # Check name valid
            err("Err: option name must be a string")
            return None
        if name not in self.opDict:
            # Check option exists
            err("Err: option "+name+" does not exist")
            return None
        if value == None:
            return self.opDict[name]
        if type(value) != type(self.opDict[name]):
            # Check value type valid
            try:
                # Try to cast as valid type
                value = type(self.opDict[name])(value)
            except:
                err("Err: type mismatch, "+str(type(self.opDict[name]))+" expected, got "+str(type(value)))
                return
        self.opDict[name] = value
        self.refresh()

    def refresh(self):
        if self.opDict["screenH"] < 200:
            self.opDict["screenH"] = 200
        if self.opDict["screenW"] < 200:
            self.opDict["screenW"] = 300
            
        ops = self.opDict
        self.screen.config(height=ops["screenH"], width=ops["screenW"], bg=ops["screenBg"])
        self.textLine.config(bg=ops["textBg"], fg=ops["textFg"], font=ops["consoleFont"])

    def getOptions(self):
        return self.opDict.copy()
                
#   --------------   CONSOLE MANAGER --------------

class ConsoleManager():
    def __init__(self, entry, canvas, host):
        self.entry = entry
        self.canvas = canvas
        self.host = host
        self.text = tk.StringVar()
        entry.bind("<Return>",self.func)
        entry.config(textvariable=self.text)
        self.count = 0

    def func(self, event=None):
        self.printText()

    def printText(self):
        text = self.submit()
        if text == "":
            return
        if text[:7] == "opcode ":
            values = text.split()
            self.host.config(values[1], values[2])
        text = "-> "+text
        self.canvas.create_text(10,10+self.count*14,text=text, fill=self.host.getOptions()["screenFg"],
                        anchor="nw", font=("Consolas",10))
        self.count += 1
        
    def submit(self):
        output = self.text.get()
        self.text.set("")
        return output

## -------------------- EMOTE CONSOLE --------------------

class EmoteConsole(CanvasConsole):
    def __init__(self, root, bdCol = "#000010", textBg = "#000000", textFg = "#FFFFFF",
                 consoleFont = ("Consolas",14), screenBg = "#003300",
                 screenFg = "#00ff00", screenW = 800, screenH = 400, emoteSize = 150):
        super().__init__(root, bdCol=bdCol, textBg=textBg, textFg=textFg, consoleFont=consoleFont,
                         screenBg=screenBg, screenFg=screenFg, screenW=screenW, screenH=screenH)
        ops = self.opDict
        ops["emoteSize"] = emoteSize
        self.screen.create_rectangle(ops["screenW"]-ops["emoteSize"],0,ops["screenW"],
                                     ops["emoteSize"],outline=ops["screenFg"])
        self.faceArr = [None, None, None]
        self.drawFace()

    def config(self, name, value=None):
        if name == "mouth":
            self.screen.delete(self.screen.find_withtag("mouth"))
            self.faceArr[1] = self.__processImage__(self.opDict["emoteSize"],
                                                  self.opDict["screenFg"],
                                                  "../assets/images/OliviaMouth"+value+".gif")
            self.screen.create_image(self.opDict["screenW"],0,image=self.faceArr[1],anchor="ne",tags="mouth")
        else:
            super().config(name, value)

    def __processImage__(self, size, color, file):
        """
        Takes a size for the returned image, a color that the image should be,
            and a reference to a black and white image to act as the mask for the color

        Returns a TK PhotoImage where the white of the mask is now color colored and
            the black is transparent
        """
        mask = Image.open(file).resize((size,size)).convert("1")
        img = Image.new("RGBA",(size,size),color)
        img.putalpha(mask)
        return ImageTk.PhotoImage(img)

    def drawFace(self):
        size = self.opDict["emoteSize"]
        self.faceArr[0] = self.__processImage__(self.opDict["emoteSize"],
                                              self.opDict["screenFg"],
                                              "../assets/images/OliviaEyes.gif")
        self.faceArr[1] = self.__processImage__(self.opDict["emoteSize"],
                                              self.opDict["screenFg"],
                                              "../assets/images/OliviaMouth1.gif")
        self.screen.create_image(self.opDict["screenW"],0,image=self.faceArr[0],anchor="ne",tags="eyes")
        self.screen.create_image(self.opDict["screenW"],0,image=self.faceArr[1],anchor="ne",tags="mouth")
        

# ------ SAMPLE CODE ------

if __name__ == "__main__":
    screenW = 400
    screenH = 300
    screenFg = "#00ff00"
    consoleFont = ("Consolas",14)
    
    app = tk.Tk()
    app.config(bd=0)
    app.resizable(False, False)
    app.title("Console")

    console = EmoteConsole(app, screenW = screenW, screenH = screenH)    
##    console.drawShape(("Oval",0+20,0+20,screenW-20,screenH-20))
##    console.clearShape(1)
##    console.drawShape(("Oval",0+30,0+30,screenW-30,screenH-30))   
##    console.drawShape(("Oval",0+20,0+20,screenW-20,screenH-20))
##    console.clearShape(1)
    console.pack()
##    console.config({"screenBg": "BLUE", "screenFg": "WHITE"})

    app.mainloop()
