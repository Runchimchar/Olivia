from TKinterConsole import CanvasConsole
import tkinter as tk

if __name__ == "__main__":
    app = tk.Tk()
    app.config(bd=0)
    app.resizable(False, False)
    app.title('Console')

    console = CanvasConsole(app, screenW = 600, screenH = 400)    
##    console.drawShape(("Oval",0+20,0+20,screenW-20,screenH-20))
##    console.clearShape(1)
##    console.drawShape(("Oval",0+30,0+30,screenW-30,screenH-30))   
##    console.drawShape(("Oval",0+20,0+20,screenW-20,screenH-20))
##    console.clearShape(1)
    console.pack()
    console.config("screenW", 200)

    app.mainloop()
