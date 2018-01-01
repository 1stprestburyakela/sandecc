from Tkinter import *
import pickle
import argparse
import CountdownClass
import ImageClass
import ImagesClass
import TweetClass
import LiveClass
import VideoClass
import os
import subprocess
import time
from tkFileDialog import askdirectory
import shutil
from random import shuffle

gui = Tk()
gui.wm_title("TV Management")
w, h = gui.winfo_screenwidth(), gui.winfo_screenheight()
gui.geometry("%dx%d+0+0" % (w, h-100))

########################  Options for things #######################
###"Name",(Class to call, buttonx, buttony),

ItemTypes = { "Image":{'type' : ImageClass},
          "Tweet":{'type' : TweetClass},
          "Countdown":{'type' : CountdownClass},
		  "MultipleImages":{'type' : ImagesClass},
          "Live":{'type' : LiveClass},
          "Video":{'type' : VideoClass}
        }

# Order to display items. These must be keys in the Items dict - if it's not in this list, it wont
# be displayed or be able to be used in any way
#ItemOrder = ["Picture", "Tweet", "Countdown"]  
FileName = "Database_Main.dat"

DatabaseName = "Main"

######################## Modify above here ####################

####### ArgParsing
parser = argparse.ArgumentParser()
parser.add_argument("--file", help="filename for database")
parser.add_argument("--db", help="database name")
args = parser.parse_args()
if args.file:
    FileName=args.file
elif args.db:
    DatabaseName = args.db
    FileName = "Database_"+DatabaseName

#######


####### Classes for ItemTypes



#######


class Shimmer(object):
    pass

######## Globals

DisplayItems = []

GridCanvas = None
GridFrame = None

########

######## Load and save

def load():
    global DisplayItems
    try:
        file = open(FileName,"rb")
        DisplayItems=pickle.load(file)
        file.close()
        print "Loaded from", FileName
        print len(DisplayItems), " items"
    except:
        print "Error loading"
        
def save():
    global DisplayItems
    try:
        file = open(FileName,"wb")
        pickle.dump(DisplayItems,file)
        file.close()
        print "Saved to", FileName
    except:
        print "Error saving"
		
def delete():
    global DisplayItems
    DisplayItems = []
    save()
    DrawItems()

def deploy():
    global DisplayItems
    
    
   
        
    deploystring = ""
    for item in DisplayItems[0:300]:
        deploystring += ItemTypes[item.config['type']]['type'].deploy(item.config)
    print deploystring
    print "Deploying"
	
    templatefile = open("Deployed\\template.html", "r")
    template = templatefile.read()
    templatefile.close()

    file = open("Deployed\\index.html", "w")

	
		
    file.write(template % deploystring)
		
    file.close()
    
    f = open("Deployed\\version.txt","w")
    f.write(str(time.time()))
    f.close()
    print "deployed"
	
def startserver():
	subprocess.Popen(["python", "server.py"])
      
# Try and load as we boot      
load()


######################


    
def DrawItems():   
        
    def CreateItemFrame(item, i):
        def MoveUp():
            global DisplayItems
            if i >0:
                DisplayItems[i-1], DisplayItems[i] = DisplayItems[i], DisplayItems[i-1]
                save()
                DrawItems()
                
        def BigUp():
            global DisplayItems
            if i >9:
                DisplayItems = DisplayItems[0:i-10] + [DisplayItems[i]] + DisplayItems[i-10:i] + DisplayItems[i+1:]
                save()
                DrawItems()
        
        def MoveDown():
            global DisplayItems
            if i < len(DisplayItems)-1:
                DisplayItems[i+1], DisplayItems[i] = DisplayItems[i], DisplayItems[i+1]
                save()
                DrawItems()
            
        def DeleteItem():
            global DisplayItems
            DisplayItems.remove(item)
            save()
            DrawItems()
            
        def EditCallback(info, config):
            item.config = config
            save()
            DrawItems()
            
        def EditItem():
            global DisplayItems
            ItemTypes[item.config['type']]['type'].WindowClass(EditCallback, item.config)
            save()
            DrawItems()
    
        itemframe = Frame(GridFrame)

        if item.config['displaytext'].lower().find('adverts') != -1:
            labelBg = "orange"
        elif item.config['type'].lower() == 'countdown':
            labelBg = "green"
        elif item.config['type'].lower() == 'tweet':
            labelBg = "lightblue"
        else:
            labelBg = "grey"

        numberlabel = Label(itemframe, text=str(i) + ".", width = "10", bg=labelBg)
        numberlabel.pack(side="left", padx ="3")
        itemlabel = Label(itemframe, text=item.config['type'] + ": " +item.config['displaytext'], width="100", anchor="w")
        itemlabel.pack(side="left", fill="x", expand=True)

        bigup = Button(itemframe, text="Big up", width="10")
        upbutton = Button(itemframe, text="Up", width= "10")
        downbutton = Button(itemframe, text="Down", width= "10")
        upbutton.pack(side="right")
        downbutton.pack(side="right")
        bigup.pack(side="right")
        
        
        deletebutton = Button(itemframe, text="Delete", width="10")
        
        editbutton = Button(itemframe, text="Edit", width="10")
        
        editbutton.pack(side="right")
        deletebutton.pack(side="right", padx ="20")      
        
        bigup['command'] = BigUp
        deletebutton['command'] = DeleteItem
        upbutton['command'] = MoveUp
        downbutton['command'] = MoveDown
        editbutton['command'] = EditItem
        
        itemframe.grid(sticky="ew", pady="5", padx ="5")

    # Clear exisiting lines
    for frame in GridFrame.winfo_children():
        frame.destroy()
    
    for i in range(0, len(DisplayItems)):
        CreateItemFrame(DisplayItems[i], i)
        
def randomize():
    shuffle(DisplayItems)
    save()
    DrawItems()
        
def commitItem(info, config):
    global DisplayItems
    print "Item committed", info
    shimmer = Shimmer()
    shimmer.config = config
    DisplayItems += [shimmer]
    save()
    DrawItems()
    
def CreateGoButton(root):
    commitFrame = Frame(root)
    commitFrame.pack(side="top")
	
    goButton = Button(commitFrame, text="Deploy", font="Helvetica 15")
    goButton.pack(side="left", padx =10, pady = 10)
    goButton['command'] = deploy
    
    shuffleButton = Button(commitFrame, text="Shuffle", font="Helvetica 15")
    shuffleButton.pack(side="left", padx =10, pady = 10)
    shuffleButton['command'] = randomize
    
    goButton = Button(commitFrame, text="Delete all", font="Helvetica 15")
    goButton.pack(side="left", padx =10, pady = 10)
    goButton['command'] = delete
	
def CreateTypeMenu(root):
    def CreateButton(typename, root):
        def ButtonClick():
            ItemTypes[typename]['type'].WindowClass(commitItem, None)
            
    
        button = Button(root, text=typename, font= "Helvetica 15")
        #button.grid(column = x, row = y, sticky = E+W )
        button.pack(side="left")
        button['command'] = ButtonClick
        
    
    buttonFrame = Frame(root)
    buttonFrame.pack(side="top",padx = 10, pady = 10)
    for name in ItemTypes:
        CreateButton(name,buttonFrame)

def GridFrameConfigure(event):
    GridCanvas.configure(scrollregion=GridCanvas.bbox("all"))
    
def GridCanvasConfigure(event):
    GridFrame.configure(width=GridCanvas.winfo_width())
    
def CreateCanvas(root):
    global GridCanvas, GridFrame
    GridCanvas = Canvas(root,borderwidth=0, background="#000000")
    GridFrame = Frame(GridCanvas, background="#ffff00")
    
    GridScroll = Scrollbar(root, orient="vertical", command=GridCanvas.yview)
    GridCanvas.configure(yscrollcommand=GridScroll.set)
    
    GridScroll.pack(side="right", fill="y")
    GridCanvas.pack(side="left", fill="both", expand=True)
    GridCanvas.create_window((4,4), window=GridFrame, anchor="nw", tags="GridFrame")
    GridFrame.bind("<Configure>", GridFrameConfigure)
    GridCanvas.bind("<Configure>", GridCanvasConfigure)

CreateGoButton(gui)
CreateTypeMenu(gui)
CreateCanvas(gui)


DrawItems()     









## Show GUI
gui.mainloop()
