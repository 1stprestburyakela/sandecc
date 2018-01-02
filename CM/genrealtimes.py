file = open("realstart.txt").readlines()

teams={}
teamtext = ""
for line in file:
    details = line.split(",")
    walkerno = int(details[1])
    if walkerno > 400:
        form = details[11][:-1]
        teamno = details[0]
        if not teamno in teams and not teamno == "":
            teams[teamno] = 1
            teamtext += "%s,%s,1,%s,,\n" % (teamno, details[9],form)
#file=open("GST1.txt", "w")
file.write(teamtext)