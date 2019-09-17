import tkinter as tk
from PIL import Image, ImageTk
from gui.TKinterConsole import CanvasConsole

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
