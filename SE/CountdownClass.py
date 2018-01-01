import Tkinter as tk
import ttk
#title, title, time, done message
template = """<div class="slide"><div class="countdown">
<h1>%s</h1>
<div id="%s"></div><script>initializeClock('%s','%s',"%s");</script>
</div></div>"""

def deploy(config):
	date = "%s %s %s %s:%s:%s GMT+0100" % (config['month'],config['day'],config['year'],config['hour'],config['min'],config['sec']) 
	return template % (config['title'].replace(' ', '-').replace("'", '-').replace('"', '-'),config['title'],config['title'],date,config['done'])


class WindowClass(tk.Toplevel):
    def __init__(self, commitFunction, currentConfig):
        tk.Toplevel.__init__(self)
        self.commitcallback = commitFunction
        self.title("Countdown item")
        
        self.slidetitlevar = tk.StringVar()
        self.slidedonevar = tk.StringVar()
        
        self.slidetitlelabel = tk.Label(self, text="Title", width="20")
        self.slidetitleentry = tk.Entry(self, width = "50", textvariable=self.slidetitlevar)    
        self.slidetitlelabel.grid(column = 0, row = 0,columnspan=1, sticky = tk.E+tk.W, padx = 2, pady = 2)
        self.slidetitleentry.grid(column = 1, row = 0,columnspan=5, sticky = tk.E+tk.W, padx = 2, pady = 2)
        
        self.slidedonelabel = tk.Label(self, text="Done Text", width="20")
        self.slidedoneentry = tk.Entry(self, width = "50", textvariable=self.slidedonevar)    
        self.slidedonelabel.grid(column = 0, row = 1,columnspan=1, sticky = tk.E+tk.W, padx = 2, pady = 2)
        self.slidedoneentry.grid(column = 1, row = 1,columnspan=5, sticky = tk.E+tk.W, padx = 2, pady = 2)
        
        
        self.slideyearlabel = tk.Label(self, text="Year", width="20")
        self.slidemonthlabel = tk.Label(self, text="Month", width="20")
        self.slidedaylabel = tk.Label(self, text="Day", width="20")
        self.slideyearvar = tk.StringVar()
        self.slidemonthvar = tk.StringVar()
        self.slidedayvar = tk.StringVar()
        
        self.slidedayoption=ttk.Combobox(self, textvariable=self.slidedayvar)
        self.slidedayoption['values'] = [x for x in range(1,32)]
        self.slidemonthoption=ttk.Combobox(self, textvariable=self.slidemonthvar)
        self.slidemonthoption['values'] = ['January', 'February', 'March', 'April', 'May', 'June', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        self.slideyearoption=ttk.Combobox(self, textvariable=self.slideyearvar)
        self.slideyearoption['values'] = [x for x in range(2016,2018)]
        
        self.slidedaylabel.grid(column = 0, row = 2,columnspan=1, padx = 2, pady = 2)
        self.slidemonthlabel.grid(column = 2, row = 2,columnspan=1, padx = 2, pady = 2)
        self.slideyearlabel.grid(column = 4, row = 2,columnspan=1, padx = 2, pady = 2)
        
        self.slidedayoption.grid(column = 1, row = 2,columnspan=1, padx = 2, pady = 2)
        self.slidemonthoption.grid(column = 3, row = 2,columnspan=1, padx = 2, pady = 2)
        self.slideyearoption.grid(column = 5, row = 2,columnspan=1, padx = 2, pady = 2)  


        
        
        self.slidehourlabel = tk.Label(self, text="Hour", width="20")
        self.slideminlabel = tk.Label(self, text="Minute", width="20")
        self.slideseclabel = tk.Label(self, text="Second", width="20")
        self.slidehourvar = tk.StringVar()
        self.slideminvar = tk.StringVar()
        self.slidesecvar = tk.StringVar()
        
        self.slidesecoption=ttk.Combobox(self, textvariable=self.slidesecvar)
        self.slidesecoption['values'] = [x for x in range(0,60)]
        self.slideminoption=ttk.Combobox(self, textvariable=self.slideminvar)
        self.slideminoption['values'] = [x for x in range(0,60)]
        self.slidehouroption=ttk.Combobox(self, textvariable=self.slidehourvar)
        self.slidehouroption['values'] = [x for x in range(0,24)]
        
        self.slidehourlabel.grid(column = 0, row = 3,columnspan=1, padx = 2, pady = 2)
        self.slideminlabel.grid(column = 2, row = 3,columnspan=1, padx = 2, pady = 2)
        self.slideseclabel.grid(column = 4, row = 3,columnspan=1, padx = 2, pady = 2)
        
        self.slidehouroption.grid(column = 1, row = 3,columnspan=1, padx = 2, pady = 2)
        self.slideminoption.grid(column = 3, row = 3,columnspan=1, padx = 2, pady = 2)
        self.slidesecoption.grid(column = 5, row = 3,columnspan=1, padx = 2, pady = 2)        
        
        
        self.commitbutton = tk.Button(self, text="Add", width=25, command=self.commit)
        self.commitbutton.grid(column = 0, row = 4,columnspan=3, sticky = tk.E+tk.W , padx = 10, pady = 10)
        self.closebutton = tk.Button(self, text="Cancel", width=25, command=self.close)
        self.closebutton.grid(column = 3, row = 4,columnspan=3, sticky = tk.E+tk.W , padx = 10, pady = 10)
        
        if currentConfig != None:            
            self.slideyearvar.set(currentConfig['year'])
            self.slidemonthvar.set(currentConfig['month'])
            self.slidedayvar.set(currentConfig['day'])
            self.slidehourvar.set(currentConfig['hour'])
            self.slideminvar.set(currentConfig['min'])
            self.slidesecvar.set(currentConfig['sec'])
            self.slidetitlevar.set(currentConfig['title'])
            self.slidedonevar.set(currentConfig['done'])

        
    
    def validate(self):
    
        self.slideyearlabel.config(fg="black")        
        self.slidemonthlabel.config(fg="black")         
        self.slidedaylabel.config(fg="black")        
        self.slidehourlabel.config(fg="black")           
        self.slideminlabel.config(fg="black")            
        self.slideseclabel.config(fg="black")
    
    
        if self.slideyearvar.get() == "":
            self.slideyearlabel.config(fg="red")
            return False
        if self.slidemonthvar.get() == "":
            self.slidemonthlabel.config(fg="red")
            return False
        if self.slidedayvar.get() == "":
            self.slidedaylabel.config(fg="red")
            return False
        if self.slidehourvar.get() == "":
            self.slidehourlabel.config(fg="red")
            return False
        if self.slideminvar.get() == "":
            self.slideminlabel.config(fg="red")
            return False
        if self.slidesecvar.get() == "":
            self.slideseclabel.config(fg="red")
            return False
        
        return True
        
        
    def commit(self):
        if (self.validate()):
        
            config = dict()
            config['type'] = "Countdown"
            config['year'] = self.slideyearvar.get()
            config['month'] = self.slidemonthvar.get()
            config['day'] = self.slidedayvar.get()
            config['hour'] = self.slidehourvar.get()
            config['min'] = self.slideminvar.get()
            config['sec'] = self.slidesecvar.get()
            config['title'] = self.slidetitlevar.get()
            config['displaytext'] = self.slidetitlevar.get()
            config['done'] = self.slidedonevar.get()
            self.commitcallback("hello", config)
            

            self.destroy()
        
    def close(self):
        self.destroy()
        

        
