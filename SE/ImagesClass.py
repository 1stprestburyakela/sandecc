import Tkinter as tk
import ttk
from tkFileDialog import askopenfilenames
import os


template = """<img src="Images/%s" class="slide" alt="Slide 1" />"""
def deploy(config):
    try:
        #newFilename = filename.replace(' ', '_').replace('"', '-').replace("'", '-')
        newFilename = filename 
        alreadydone = os.listdir("Images")
        fullpath = config['filepath']
        print fullpath
        folder = os.path.basename(os.path.dirname(fullpath))
        #print folder
        filename = folder+os.path.basename(fullpath)
        if "resized"+newFilename not in alreadydone:
            print "Resizing", filename
            os.system("magick "+fullpath+" -auto-orient -resize 1920x1080 Images\\resized"+newFilename )
			
        return template % ("resized"+filename)
    except:
        return ""


def outputline(config):
    # todo output some stuff
    return """<img src="%s" alt="Slide 1" />""" % config['filepath']

class WindowClass(tk.Toplevel):

    def pickfile(self):
        file_opts = {'initialdir': 'E:\\Photos'}
        filename = list(askopenfilenames(**file_opts))
        self.slidefilepathsvar.set(filename)
        print filename
        if filename != "":
            self.commit()
            
    def preview(self):
		pass
         

    def __init__(self, commitFunction, currentConfig):
        tk.Toplevel.__init__(self)
        self.commitcallback = commitFunction
        self.title("Image item")
        
        #
        #
        
        self.slidefilepathsvar = tk.StringVar()
        
        
        self.slidetitlelabel = tk.Label(self, text="Filepaths", width="15")
        self.slidetitleentry = tk.Entry(self, width = "50", textvariable=self.slidefilepathsvar)
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
            self.slidefilepathsvar.set(currentConfig['filepath'])
            
        
    
    def validate(self, filename):
        print "Validating ", filename
        return os.path.isfile(filename)
        
        
        
    def commit(self):
        #filenames = self.tk.splitlist(self.slidefilepathsvar.get())
        filenames = eval(self.slidefilepathsvar.get())
        validated = True
        print "Filenames", filenames
        for filename in filenames:
            valid = self.validate(filename)
            validated &= valid
            if not valid:
                print filename, "Failed to validate"
            
            
        if (validated):
            for filename in filenames:
                config = dict()
                config['type'] = "Image"
                config['filepath'] = filename
                config['displaytext'] = filename
                self.commitcallback("hello", config)
            self.destroy()
        
    def close(self):
        self.destroy()
        

        
