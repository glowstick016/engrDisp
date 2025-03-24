import tkinter as tk #Need for display
from PIL import Image, ImageTk #Needed for image conversion
import os #Used for file checks

#Defining the class for opening an image 
class win:
    def __init__(self, path, pauseTime):
        #Variables for the image itself
        self.image = None 
        self.path = path
        self.time = pauseTime
        
        #Variables for the display size
        self.width = None 
        self.height = None 
        
        #Variables for the images
        self.root = tk.Tk()
        
    #Creating the window function
    def startWin(self):
        try:
            
            #Getting the height and width of the screen & Prep the image
            self.width = self.root.winfo_screenwidth()
            self.height = self.root.winfo_screenheight()
            
            self.prepImage()
            
            if (self.image == None or self.width == None or self.height == None):
                print("Failed after prep image")
                #Failed to do a requirement 
            else:
                print(self.width, self.height)
            
            #start function
            self.root.mainloop()
            

        except Exception as error:
            print("Error in display.py with win.startWin: ", type(error).__name__, "–", error)
        
    def closeWin(self):
        try:
            if(self.root):
                self.root.destroy()
        except Exception as error:
            print("Error in display.py with win.closeWin: ", type(error).__name__, "–", error)
        
    
    #Functions to handle the images
    def prepImage(self):
        try:
            
            if(os.path.isfile(self.path)):
                #Goal is to get the image and resize as needed 
                self.image = Image.open(self.path)
                
                #Resizing and converting         
                self.image = self.image.resize((self.width, self.height), Image.Resampling.LANCZOS)
                self.image = ImageTk.PhotoImage(self.image)
                
                #Setting a label for display
                self.label = tk.Label(self.root, image=self.image)
                self.label.pack()
                
                #Fullscreen
                self.root.attributes('-fullscreen', True)
                self.root.bind('<Escape>', lambda _: self.closeWin())
            else:
                print("Can't open file")
        except Exception as error:
            print("Error in display.py with win.preImage: ", type(error).__name__, "–", error)