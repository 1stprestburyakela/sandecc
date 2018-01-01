import Tkinter as tk
import ttk
#title, title, time, done message
template = """<div class="slide">
<div class="twitterleft"><img src="twitterlogo.png" height="300px" width="300px"/></div>
<div class="twitterright">
<h1>%s</h1>
<h2>%s</h2>
</div>

</div>"""

def deploy(config):
	
	return template % (config['uname'],config['content'],)


class WindowClass(tk.Toplevel):
    def __init__(self, commitFunction, currentConfig):
        tk.Toplevel.__init__(self)
        self.commitcallback = commitFunction
        self.title("Countdown item")
        
        self.slidenamevar = tk.StringVar()
        self.slideunamevar = tk.StringVar()
        self.slidecontentvar = tk.StringVar()
        
        self.slidenamelabel = tk.Label(self, text="Name", width="20")
        self.slidenameentry = tk.Entry(self, width = "50", textvariable=self.slidenamevar)    
        self.slidenamelabel.grid(column = 0, row = 0,columnspan=1, sticky = tk.E+tk.W, padx = 2, pady = 2)
        self.slidenameentry.grid(column = 1, row = 0,columnspan=5, sticky = tk.E+tk.W, padx = 2, pady = 2)
        
        self.slideunamelabel = tk.Label(self, text="User name", width="20")
        self.slideunameentry = tk.Entry(self, width = "50", textvariable=self.slideunamevar)    
        self.slideunamelabel.grid(column = 0, row = 1,columnspan=1, sticky = tk.E+tk.W, padx = 2, pady = 2)
        self.slideunameentry.grid(column = 1, row = 1,columnspan=5, sticky = tk.E+tk.W, padx = 2, pady = 2)
        
        self.slidecontentlabel = tk.Label(self, text="Content", width="20")
        self.slidecontententry = tk.Entry(self, width = "100", textvariable=self.slidecontentvar)    
        self.slidecontentlabel.grid(column = 0, row = 2,columnspan=1, sticky = tk.E+tk.W, padx = 2, pady = 2)
        self.slidecontententry.grid(column = 1, row = 2,columnspan=5, sticky = tk.E+tk.W, padx = 2, pady = 2)
        
        
          
        
        
        self.commitbutton = tk.Button(self, text="Add", width=25, command=self.commit)
        self.commitbutton.grid(column = 0, row = 4,columnspan=3, sticky = tk.E+tk.W , padx = 10, pady = 10)
        self.closebutton = tk.Button(self, text="Cancel", width=25, command=self.close)
        self.closebutton.grid(column = 3, row = 4,columnspan=3, sticky = tk.E+tk.W , padx = 10, pady = 10)
        
        if currentConfig != None:            
            self.slidenamevar.set(currentConfig['name'])
            self.slideunamevar.set(currentConfig['uname'])
            self.slidecontentvar.set(currentConfig['content'])
            

        
    
    def validate(self):
    
        
        return True
        
        
    def commit(self):
        if (self.validate()):
        
            config = dict()
            config['type'] = "Tweet"
            config['name'] = self.slidenamevar.get()
            config['uname'] = self.slideunamevar.get()
            config['content'] = self.slidecontentvar.get()
            config['displaytext'] = self.slidenamevar.get()
            self.commitcallback("hello", config)
            self.destroy()
        
    def close(self):
        self.destroy()
        

        
