import Tkinter as tk
import ttk
from tkFileDialog import askopenfilename
import os


template = """<img src="http://192.168.20.20:9000/stream/video.jpeg" class="slide" alt="Slide 1%s" data-trans="setTimeout(function(){transition();}, 15000)"/>"""
def deploy(config):
    #try:
        #newFilename = filename.replace(' ', '_').replace('"', '-').replace("'", '-')
        
        
        return template % config['path']
    #except:
        return ""




def outputline(config):
    # todo output some stuff
    returntemplate % config['filepath']

class WindowClass(tk.Toplevel):

   
            
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
        #self.slidefilebutton = tk.Button(self, text="...", width="10", command=self.pickfile)
        self.slidetitlelabel.grid(column = 0, row = 0,columnspan=1, sticky = tk.E+tk.W, padx = 2, pady = 2)
        self.slidetitleentry.grid(column = 1, row = 0,columnspan=4, sticky = tk.E+tk.W, padx = 2, pady = 2)
        #self.slidefilebutton.grid(column = 5, row = 0,columnspan=1, sticky = tk.E+tk.W, padx = 2, pady = 2)
        
        
        #self.slidefilebutton = tk.Button(self, text="Preview", width="10", command=self.preview)
        #self.slidefilebutton.grid(column = 0, row = 1,columnspan=6, sticky = tk.E+tk.W , padx = 10, pady = 10)
        
        
        self.commitbutton = tk.Button(self, text="Add", width=25, command=self.commit)
        self.commitbutton.grid(column = 0, row = 2,columnspan=3, sticky = tk.E+tk.W , padx = 10, pady = 10)
        self.closebutton = tk.Button(self, text="Cancel", width=25, command=self.close)
        self.closebutton.grid(column = 3, row = 2,columnspan=3, sticky = tk.E+tk.W , padx = 10, pady = 10)
        
        if currentConfig != None:            
            self.slidefilepathvar.set(currentConfig['path'])
            
        
    
    def validate(self):
        return True
        
        
        
    def commit(self):
        if (self.validate()):
            for x in range (0,10):
                config = dict()
                config['type'] = "Live"
                config['path'] = self.slidefilepathvar.get()
                config['displaytext'] = "Live :"+  self.slidefilepathvar.get()
                self.commitcallback("hello", config)
            self.destroy()
        
    def close(self):
        self.destroy()
        

        
