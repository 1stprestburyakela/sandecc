import Tkinter as tk
import ttk
from tkFileDialog import askopenfilename
import os
import shutil
import random


template = """
<video class='slide' id='%s' data-trans="x = document.getElementById('%s');x.onended=function(){transition()}; x.play(); ;">
    <source src="Images/%s" type='video/mp4; codecs="avc1.4D401E, mp4a.40.2"'>
</video>
"""
def deploy(config):
    #try:
        #newFilename = filename.replace(' ', '_').replace('"', '-').replace("'", '-')
        
        alreadydone = os.listdir("Deployed\\Images")
        fullpath = config['filepath']
        print fullpath
        folder = os.path.basename(os.path.dirname(fullpath))
        #print folder
        filename = folder+os.path.basename(fullpath)
        newFilename = filename.replace(' ', '_').replace('"', '-').replace("'", '-')
        
        #//shutil.copy(fullpath, os.path.join("Deployed\\Images", newFilename))
        
        id = "videoid"+str(random.randint(0,1000))
        
        return template % (id,id, newFilename)
    #except:
        return ""




def outputline(config):
    # todo output some stuff
    return """<img src="%s" alt="Slide 1" />""" % config['filepath']

class WindowClass(tk.Toplevel):

    def pickfile(self):
        file_opts = {'initialdir': 'E:\\Photos'}
        filename = askopenfilename(**file_opts)
        self.slidefilepathvar.set(filename)
        print filename
        if filename != "":
            self.commit()
            
    def preview(self):
        if (self.validate()):
            os.startfile(self.slidefilepathvar.get())    

    def __init__(self, commitFunction, currentConfig):
        tk.Toplevel.__init__(self)
        self.commitcallback = commitFunction
        self.title("Image item")
        
        #
        #
        
        self.slidefilepathvar = tk.StringVar()
        
        
        self.slidetitlelabel = tk.Label(self, text="Filepath", width="15")
        self.slidetitleentry = tk.Entry(self, width = "50", textvariable=self.slidefilepathvar)
        self.slidefilebutton = tk.Button(self, text="...", width="10", command=self.pickfile)
        self.slidetitlelabel.grid(column = 0, row = 0,columnspan=1, sticky = tk.E+tk.W, padx = 2, pady = 2)
        self.slidetitleentry.grid(column = 1, row = 0,columnspan=4, sticky = tk.E+tk.W, padx = 2, pady = 2)
        self.slidefilebutton.grid(column = 5, row = 0,columnspan=1, sticky = tk.E+tk.W, padx = 2, pady = 2)
        
        
        self.slidefilebutton = tk.Button(self, text="Preview", width="10", command=self.preview)
        self.slidefilebutton.grid(column = 0, row = 1,columnspan=6, sticky = tk.E+tk.W , padx = 10, pady = 10)
        
        
        self.commitbutton = tk.Button(self, text="Add", width=25, command=self.commit)
        self.commitbutton.grid(column = 0, row = 2,columnspan=3, sticky = tk.E+tk.W , padx = 10, pady = 10)
        self.closebutton = tk.Button(self, text="Cancel", width=25, command=self.close)
        self.closebutton.grid(column = 3, row = 2,columnspan=3, sticky = tk.E+tk.W , padx = 10, pady = 10)
        
        if currentConfig != None:            
            self.slidefilepathvar.set(currentConfig['filepath'])
            
        
    
    def validate(self):
        return os.path.isfile(self.slidefilepathvar.get())
        
        
        
    def commit(self):
        if (self.validate()):
        
            config = dict()
            config['type'] = "Video"
            config['filepath'] = self.slidefilepathvar.get()
            config['displaytext'] = self.slidefilepathvar.get()
            self.commitcallback("hello", config)
            self.destroy()
        
    def close(self):
        self.destroy()
        

        
