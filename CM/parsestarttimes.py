
names = open("formstoname.csv").readlines()
uptimestart = ""
uptimestarttempplate = """upTime('feb,04,2017,%s:%s:%s', '%s');\n"""
fixtimestarttempplate = """fixTime('feb,04,2017,%s:%s:%s','feb,%s,2017,%s:%s:%s', '%s');\n"""
html = ""
htmltemplate = """<div id="countup">
  <p>%s have taken</p>
  <p id="%shours">00</p>
  <p class="timeRefHours">hours</p>
  <p id="%sminutes">00</p>
  <p class="timeRefMinutes">minutes</p>
  <p id="%sseconds">00</p>
  <p id="%ssecondstag" class="timeRefSeconds">seconds so far and have got past CP %s</p>
  </div>"""
htmlnexttemplate = """<div id="countupnex">
  <p>%s have taken</p>
  <p id="%shours">00</p>
  <p class="timeRefHours">hours</p>
  <p id="%sminutes">00</p>
  <p class="timeRefMinutes">minutes</p>
  <p id="%sseconds">00</p>
  <p id="%ssecondstag" class="timeRefSeconds">seconds so far and have got past CP %s</p>
  </div>"""

htmlrettemplate = """<div id="countupret">
  <p>%s kept going for</p>
  <p id="%shours">00</p>
  <p class="timeRefHours">hours</p>
  <p id="%sminutes">00</p>
  <p class="timeRefMinutes">minutes</p>
  <p id="%sseconds">00</p>
  <p id="%ssecondstag" class="timeRefSeconds">second</p>
</div>"""

htmlfintemplate = """<div id="countupfin">
  <p>%s finished in</p>
  <p id="%shours">00</p>
  <p class="timeRefHours">hours</p>
  <p id="%sminutes">00</p>
  <p class="timeRefMinutes">minutes</p>
  <p id="%sseconds">00</p>
  <p id="%ssecondstag" class="timeRefSeconds">second</p>
</div>"""

gn = {}
for line in names:
    linesplit = line.split("#")
    entryform = linesplit[0]
    groupname = linesplit[6]
    gn[entryform] = groupname
    print entryform,groupname



file = open("GST1.txt").readlines()

for line in file:
    details = line.split(",")
    name = details[0]
    form = details[3]
    time = details[1][11:]
    hour = time[0:2]
    min = time[3:5]
    sec = time[6:8]
    if name == "\n":
        break
    print gn[form], time, hour, min, sec
    status = details[4]
    endtime = details[5]
    endday= endtime[9:11]
    endhour = endtime[0:2]
    endmin = endtime[3:5]
    endsec = endtime[6:8]
    cp = details[7]
    
    if (status == "wal"):
        html += htmltemplate % (gn[form], name,name,name,name,cp)
        uptimestart += uptimestarttempplate % (hour,min,sec,name)
    if (status == "nex"):
        html += htmlnexttemplate % (gn[form], name,name,name,name,cp)
        uptimestart += uptimestarttempplate % (hour,min,sec,name)
    elif (status == "ret"):
        html += htmlrettemplate % (gn[form], name,name,name,name)
        uptimestart += fixtimestarttempplate % (hour,min,sec,endday,endhour,endmin,endsec,name)
    elif (status == "fin"):
        html += htmlfintemplate % (gn[form], name,name,name,name)
        uptimestart += fixtimestarttempplate % (hour,min,sec,endday,endhour,endmin,endsec,name)  
    
    
    
page = open("timepage.template").read()

print page
page = page%(uptimestart, html)

newpage = open("timepage.html","w")
print page
newpage.write(page)

    

    
    