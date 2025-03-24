#Importing required packages
import time #Needed for sleep command 
import threading  #Needed for Multithreading
from datetime import datetime #Needed to get current time

#Custom python scripts
from databaseCon import * 
from display import * 

#Should work with jpeg, png, gif, bmp, tiff
#Need to chagne to video but that requires some of the database to be done 





class main:
    #Goal is to call everything needed and handle the threads/children
    def __init__(self, path, pauseTime):
        #Setting variables needed for constant running
        self.count = 0
        self.active = []
        self.inactive = None
        
        #Variables for the image itself
        self.path = path
        self.time = pauseTime
        
        #Variables needed for second image
        self.tmp_Path = None
        self.sec_Time = None
        
        #Variables for swap
        self.swap = False
        self.time_swap = False
        
        #Setting the subclasses
        self.display1 = win(self.path,self.time)
        self.display2 = None
        
    def start_session(self):
        try:
                
            #Creating the threads
            self.activate_thread = threading.Thread(target= self.updateActive)
            self.timer_thread = threading.Thread(target= self.imgCount)
            
            self.activate_thread.start()
            self.timer_thread.start()
            
            self.display1.root.after(((self.time + 1) * 1000),self.swapImage)
            
            #Making the main window
            self.display1.startWin()
        except Exception as error:
            print("Error in display.py main.start_session: ", type(error).__name__, "-", error)

            
    #Functions to handle the second image
    def imgCount(self):
        #Goal is to start the image prep and count down time for the timeThread
        try:
            #Need to incorporate a sleep delay for startup
            while(True):        
                #Sleep for the time and then swap the image
                time.sleep(self.time)
                self.time_swap = True
                
        except Exception as error:
            print("Error in display.py with win.imgCount: ", type(error).__name__, "–", error)
        
        
    def secPrep(self):
        #Goal is to do all the work to prep the next image
        try:  
            print("secPrep Called, len: ", len(self.active)) 
            if(len(self.active) < 1):
                #table is empty continue displaying engineering image
                self.tmp_Path = self.path
                self.sec_Time = self.time
                
                
            elif(len(self.active) == self.count):
                #Need to set count back to 1 and start the process again
                print("reset count")
                self.count = 0
                
                #Getting all of the variables set 
                self.tmp_Path = self.active[self.count]['dispTable_Path'] + self.active[self.count]['dispTable_Name']
                self.sec_Time = self.active[self.count]['dispTable_Delay']
                
            
            else:
                #Need to increment to the next size
                print("Adding to count")
                
                #Getting all of the variables set 
                self.tmp_Path = self.active[self.count]['dispTable_Path'] + self.active[self.count]['dispTable_Name']
                self.sec_Time = self.active[self.count]['dispTable_Delay']

                
                self.count += 1
                    

                
        except Exception as error:
            print("Error in display.py with win.secPrep: ", type(error).__name__, "–", error)
            
    def swapImage(self):
        #Goal is to swap the image up right now with the next image
        try:
            #Check if the time is right for swapping
            if(self.time_swap):
                
                self.secPrep()
                #Converting temp varialbes to main ones
                self.path = self.tmp_Path
                self.time = self.sec_Time
                print(self.time, self.path)
                
                if(self.display2 == None):
                    #Need to break display1
                    self.display1.closeWin()
                    self.display1 = None
                    
                    self.display2 = win(self.path, self.time)
                    
                    #Check that it actually broke
                    if(self.display1 == None):
                        time.sleep(1)
                        #Start new image
                        #self.display1 = win(self.path, self.time)
                        self.display2.root.after((self.time * 1000),self.swapImage)
                        self.display2.startWin()
                        
                elif(self.display1 == None):
                    self.display2.closeWin()
                    self.display2 = None
                    
                    self.display1 = win(self.path, self.time)
                    
                    if(self.display2 == None):
                        time.sleep(1)
                        
                        self.display1.root.after((self.time * 1000), self.swapImage)
                        self.display1.startWin()
                
                self.time_sleep = False
                    
            else:
                print("Nope")
        except Exception as error:
            print("Error in display.py with main.swapImage: ", type(error).__name__, "-", error)           
                
                
    #Functions to update the table for active status
    def updateActive(self):
        try:
            #Goal is to handle the updating of what is the activeImages on display
            sleepTime = 1 #Specify in minutes
            currTime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            currTime = datetime.strptime(currTime, '%Y-%m-%d %H:%M:%S')
            tmpActive = []
            
            #Making the thread to update the inactive
            inactiveThread = threading.Thread(target = self.updateInactive, args = (currTime,))
            inactiveThread.start()
            
            #Need to update self variables
            unsorted_active = getActive()

            
            #Need to update the class database then remove all none active based on date
            for image in unsorted_active:
                
                #Will need to change once the sql is properly set to include the time 
                imgDeploy = datetime.combine(image["imgDeploy"], datetime.min.time())
                imgRetire = datetime.combine(image["imgRetire"], datetime.min.time())
                
                #Check if current time is in the boundaries
                if ( imgDeploy <= currTime and imgRetire >= currTime):
                    tmpActive.append(image)
                else:
                    changeActive(image["imgName"], 0)
                    
                    
            #Updating values
            self.active = tmpActive

            
            #Call itself to continue to the process & thread after the delay
            time.sleep(sleepTime)
            inactiveThread.join()
            self.updateActive()
            
        except Exception as error:
            print("Error in display.py with win.updateActive: ", type(error).__name__, "–", error)



    def updateInactive(self,currTime):
        #Goal is to update all the inactive to active        
        try:
            #Getting the inactive values in the database
            tmpInactive = getInactive()
            
            #Need to go through all of them and check if the time is right
            for image in tmpInactive:
                
                #print("Inactive: ", image)
                
                #Getting the right vairables
                imgDeploy = datetime.combine(image["imgDeploy"], datetime.min.time())
                imgRetire = datetime.combine(image["imgRetire"], datetime.min.time())
                
                if (imgDeploy <= currTime and imgRetire >= currTime):
                    #Need to change to active
                    changeActive(image["imgName"],1)
        
        except Exception as error:
            print("Error in display.py with win.updateInactive: ", type(error).__name__, "–", error)

        
        
        
if __name__ == "__main__":
    #Need to change to get the right file + time from database 
    display = main("/home/cjkenned/engrDisp/clientSide/images/test.jpg", 5)
    display.start_session()
    