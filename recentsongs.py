import xml.etree.ElementTree as ElementTree
import datetime as DT
import os
import glob
import re
from collections import defaultdict
from songreplacements import songreplacements
from mako.template import Template
from mako.lookup import TemplateLookup
from config import *

print('\t\tCalculating website')

def maybereplacesong(song):
    if song in songreplacements:
        return songreplacements[song]
    else:
        return song

# __________________ CONFIGURATION _________________



mylookup = TemplateLookup(directories=[makotemplates],
                          module_directory=makomodules,
                          strict_undefined=True)

# ______________________DATES_______________________

def getdate(datestring,usingformat = filedateformat):
    datelen = len(DT.date.today().strftime(usingformat))        #how long this format is
    thedatestamp = DT.datetime.strptime(datestring[0:datelen],usingformat) #read the datelen prefix as a datetime
    thedate = DT.date(thedatestamp.year,thedatestamp.month,thedatestamp.day) #convert to a date
    return thedate

today = DT.date.today()
epoch = DT.date(1970,1,1)
recentDates = {period:today - DT.timedelta(recentDays[period])
               for period in recentDays}
if includeAllTimeInRecents:
    recentDates[includeAllTimeInRecents]=epoch
newnessStarts = today - DT  .timedelta(365.25 * yearsAgoThatNewnessStarts)
datePeriods = recentDates.keys()
        
# _____________________SONG FILES__________________________

sundayFiles = glob.glob(oldsetsglob)
sundayFiles.extend(glob.glob(newsetsglob))
songFiles = glob.glob(songglob)
                 
# ___________________ Sundays and Songs ___________________

sundays = defaultdict(list)
songs = defaultdict(list)

def songsIn(pathtosongset):
   root = ElementTree.parse(pathtosongset).getroot()            #parse xml
   for sg in root.findall("slide_groups/slide_group"): #songs are slide groups
       if sg.get("type") == "song":                    #only songs
           songname = maybereplacesong(sg.get("name"))
           yield maybereplacesong(songname)            #yield is return but makes an iterator rather than a standard funtion

notnew   = [song for song in songsIn(notnewpath)]
notsongs = [song for song in songsIn(notsongspath)]                

for file in sundayFiles:
    sunday = getdate(os.path.basename(file))            #get date from filename
    for song in songsIn(file):
        if song not in notsongs:
            sundays[sunday].append(song)            #this sunday we sang this song
            songs[song].append(sunday)              #we sang this song this sunday




def glance(myDict):
    return dict([(key, myDict[key]) for key in sorted(myDict.keys())[:3]])
#print(glance(sundays))
#print(glance(songs))


# _____________________ Date ranges _______________________

class Dates(object):
    def __init__(self,datelist):
        self.dates =[d.isoformat() for d in reversed(sorted(datelist))]
        self.number = len(self.dates)
    def __str__(self):
        return "Dates("+str(self.number)+",["+", ".join(self.dates)+"])"
    def __repr__(self):
        return "Dates("+str(self.number)+",["+", ".join(self.dates)+"])"
        
def songNewOnDate(songfilename,date):
    if songfilename in notnew:
        return ""
    elif not songs[songfilename]:
        return "never"
    elif date == min(songs[songfilename]) and date > newnessStarts:
        return "new"
    else:
        return ""

def mapisoformat(alistoflists):
    return [[l.isoformat() for l in alist] for alist in alistoflists]

def justSince(listofdates,since):
    dates = [date for date in listofdates if date >= since]
    return Dates(dates)

recentPeriodMaximums = {period:0 for period in recentDates}

def recentDatesOf(songfilename):    #updates recentPeriodMaximums as a side effect
    dates = songs[songfilename]
    recent = {}
    for period in datePeriods:
        recent[period] = justSince(dates,recentDates[period])
        howmany = recent[period].number
        if howmany > recentPeriodMaximums[period]:
            recentPeriodMaximums[period] = howmany
    return recent

# ________________________ Song Numbers ____________________

def vlookup(value,assoclist):
    answer = None
    for lowerbound in (sorted(assoclist.keys())):
        if (value >= lowerbound):
            answer = assoclist[lowerbound]
    return answer

def bookNo(songnumber):
    if (songnumber.isnumeric()):
        return vlookup(int(songnumber),whichSoF) or ""
    elif songnumber[0:2] == "HP":
        return "HP"
    else:
        return ""
    
songnumberNameRE = re.compile('^(\d*) (.+)$|^(HP\d+) (.+)$')
hpRE = re.compile('^(HP\d+) (.+)$')

def numberFromFileName(songfilename):
    result = songnumberNameRE.match(songfilename)
    if result:
        return result.group(1) or result.group(3)
    else:
        return ""

def songnameFromFileName(songfilename):
    result = songnumberNameRE.match(songfilename)
    if result:
        return result.group(2) or result.group(4)
    else:
        return songfilename
    

# ________________________ Songs ___________________________

class SongHistory(object):
    def __init__(self,
                 songfilename="Error:song filename not supplied",   #Required
                 recentTimes={}):                           #calculated
        self.songfilename = songfilename
        self.recentTimes = recentDatesOf(songfilename)
        m = songnumberNameRE.match(songfilename)
        if m:
            self.songnumber = m.group(1) or m.group(3)
            self.songtitle = m.group(2) or m.group(4)
        else:
            self.songnumber = ""
            self.songtitle = songfilename
     

        selfsongnumber = songfilename[0:4]
        if selfsongnumber.isdigit():
            selfsongtitle = songfilename[5:]
        else:
            maybeHPmatch = hpRE.match(songfilename)
            if maybeHPmatch:
                selfsongnumber = maybeHPmatch.group(1)
                selfsongtitle = maybeHPmatch.group(2)
            else:
                selfsongtitle = songfilename
                selfsongnumber = ''
        if not selfsongnumber== self.songnumber:
            print (selfsongnumber+" "+self.songnumber)

    def __repr__(self):
        return("SongHistory"
               +"(songfilename='"+self.songfilename
               +"',recentTimes="+str(self.recentTimes)
               +")")



class SongOnDate(SongHistory):
    def __init__(self,
                 songfilename="Error:song filename not supplied",   #Required
                 date="1970-01-01",                         #Required
                 newToday="?",                              #calculated
                 recentTimes={}):                           #calculated
        SongHistory.__init__(self,songfilename)
        if isinstance(date,DT.date):
            self.date = date
        else:
            self.date = getdate(date,"%Y-%m-%d")
        self.newToday = songNewOnDate(songfilename, self.date)

    def __repr__(self):
        return("SongOnDate"
               +"(songfilename='"+self.songfilename
               +"',date='"+str(self.date)
               +"',newToday='"+self.newToday
               +"',recentTimes="+str(self.recentTimes)
               +")")

# ________________________ Tables ___________________________

actualSongFiles = [song for song in
                   (os.path.basename(file) for file in songFiles)
                   if song not in notsongs]

songListFromFiles = list(map(maybereplacesong,actualSongFiles))

songsWithoutSongFiles = [song for song in sorted(songs)
                         if song not in songListFromFiles]

if songsWithoutSongFiles:
    print('_____________________ Missing songs report ____________________')
    print('   There are no actual song files for the following songs.     ')
    print('Please complete the lines below and save in songreplacements.py')
    for song in songsWithoutSongFiles:
        print('"'+song+'":"",')
    print('_______________________________________________________________')
    print('You could run localsongutils.py and then open MissingSongs.html')
    print('______________ End of missing songs report ____________________')



ourSongsTable = [SongHistory(song) for song in sorted(songs)]
for song in songListFromFiles:                              #Add songs that haven't been used
    if not song in songs and song not in notsongs:
        songs[song]=[]
allSongsTable = [SongHistory(song) for song in sorted(songs)]
sundayTable = []
for date in reversed(sorted(sundays.keys())):
    sundayTable.extend([SongOnDate(song,date) for song in sundays[date]])


# _______________________________ USER INTERFACE _______________________________
# _______________________________ USER INTERFACE _______________________________
# _______________________________ USER INTERFACE _______________________________
# _______________________________ USER INTERFACE _______________________________
# _______________________________ USER INTERFACE _______________________________
# _______________________________ USER INTERFACE _______________________________
# _______________________________ USER INTERFACE _______________________________

# ___________________ COLOURS _________________________
def colourDate(date):
    return dateColour.format(date.day*10)

def colourFrequency(period,freqs):
    no = freqs[period].number
    maxno = max(recentPeriodMaximums[period],1)
    lum = 100 - no / maxno * (100 - minLuminosity)  # 100 when no=0, minLuminosity when no=maxno  
    return frequencyColour.format(int(round(lum)))  # eg hsl(135, 50%, 30%)

# ___________________ Sort orders by frequency ________________
# We'll multiply the frequencies by 10 to a power and sum.
# We use higher powers to emphasise that period above others in the sort order

powerDictDict = {"three months":
                            {"three months":7,
                             "six months":5,
                             "year":3,
                             "All time":0},
                 "six months":
                            {"three months":5,
                             "six months":7,
                             "year":3,
                             "All time":0},
                 "year":
                            {"three months":3,
                             "six months":5,
                             "year":7,
                             "All time":0},
                 "All time":
                            {"three months":0,
                             "six months":2,
                             "year":4,
                             "All time":6}
                 }

def sortFunctionFromPeriod(period):
    def sortFunction(song):
        total=0;
        for p in datePeriods:
            total += (song.recentTimes[p].number
                      * 10**powerDictDict[period][p])
        return total
    return sortFunction

# ____________________ FILENAMES _______________________
templatesUsed = {"New":         "bydate.html",
                 "Date":        "bydate.html",
                 "Song":        "bydate.html",
                 "No.":         "bydate.html",
                 "Non-SoF new": "bydate.html",
                 "December":    "bydate.html",
                 "Test":    "test.html"}
for period in datePeriods:
    templatesUsed[period]="bydate.html"


def outputfilename(button,forwards):
    trunk = re.sub('[^A-Za-z0-9_-]', '_', button)
    if forwards:
        return "by_"+trunk+".html"
    else:
        return "by_"+trunk+"_backwards.html"

def buttonLinks(frombutton,forwards):
    links = {}
    for tobutton in templatesUsed.keys():
        if tobutton==frombutton:
            links[tobutton]=outputfilename(tobutton,not forwards)
        else:
            links[tobutton]=outputfilename(tobutton,True)
    return links

linksOnHomepage = {"Date":"Date",
                   "Song":"Song",
                   "New":"New",
                   "Number":"No.",
                   "Most used":"All time",
                   "Non-SoF new":"Non-SoF new",
                   "December songs":"December"}
                   

# _______________________ IDs ________________________

def makeID(sometext):
    return re.sub('[^A-Za-z0-9_-]', '', sometext)+'ID'
            # Only keep alphanumeric or _ - 




#                                                                    
# ____________________________ PAGES ________________________________
#                                                                    

class Page(object):
    def __init__(self,
                 button,        #What we clicked
                 forwards,      #Is this the officially forwards version, or did we click a second time?
                 sortfunction,  #Lambda to return the field tuple to sort on             
                 usereversed,   #Should we reverse after using the sortfunction?
                 hasDates,      #True to use sundayTable, false to put blanks in the New and Date columns
                 underlyingTable=[],  #Underlying table of SongHistory or SongOnDate
                 onlyif=lambda x:True,  #Lambda to keep records
                 template="bydate.html",        #calculated from Button
                 filename="unnamedpage.html"    #calculated from Button&forwards
                 ):
        self.button=button
        self.forwards=forwards
        self.sortfunction=sortfunction
        self.usereversed=usereversed
        self.hasDates=hasDates
        self.template=templatesUsed[button]
        self.filename=outputfilename(button,forwards)
        self.onlyif=onlyif
        self.underlyingTable=underlyingTable

    def __repr__(self):
        return ("Page"+
                "(button='"+self.button+
                "',forwards='"+repr(self.forwards)+
                "',sortfunction="+repr(self.sortfunction)+
                "',usereversed='"+repr(self.usereversed)+
                "',hasDates='"+repr(self.hasDates)+
                "',template='"+self.template+
                "',filename='"+self.filename+
                ")")
# Adding pages:
# Make an entry here, and in the templatesUsed dictionary.
# Probably add it into linksOnHomepage too.

pages = [
    Page(button="Date",
         underlyingTable=sundayTable,
         forwards=True,
         sortfunction=None,
         usereversed=False,
         hasDates=True),
    Page(button="Date",
         underlyingTable=sundayTable,
         forwards=False,
         sortfunction=lambda x:x.date,  # Weirdly, this does the right thing
         usereversed=False,             # when we don't reverse it
         hasDates=True),
    Page(button="New",
         underlyingTable=sundayTable,
         forwards=True,
         sortfunction=lambda x: (x.date, x.songfilename.lower()),
         usereversed=True,
         onlyif=lambda x:x.newToday.lower()=="new",
         hasDates=True),
    Page(button="New",
         underlyingTable=sundayTable,
         forwards=False,
         sortfunction=lambda x: (x.date, x.songfilename.lower()),
         usereversed=False,
         onlyif=lambda x:x.newToday.lower()=="new",
         hasDates=True),
    Page(button="Song",
         underlyingTable=allSongsTable,
         forwards=True,
         sortfunction=lambda x: x.songtitle.lower(),
         usereversed=False,
         hasDates=False),
    Page(button="Song",
         underlyingTable=allSongsTable,
         forwards=False,
         sortfunction=lambda x: x.songtitle.lower(),
         usereversed=True,
         hasDates=False),
    Page(button="No.",
         underlyingTable=allSongsTable,
         forwards=True,
         sortfunction=lambda x: x.songnumber+"zzzzzz"+x.songtitle.lower(),
         usereversed=False,
         hasDates=False),
    Page(button="No.",
         underlyingTable=allSongsTable,
         forwards=False,
         sortfunction=lambda x: x.songnumber+"zzzzzz"+x.songtitle.lower(),
         usereversed=True,
         hasDates=False),
    Page(button="Non-SoF new",
         underlyingTable=sundayTable,
         forwards=True,
         sortfunction=lambda x: (x.date, x.songfilename.lower()),
         usereversed=True,
         onlyif=lambda x:x.newToday.lower()=="new" and x.songnumber=='',
         hasDates=True),
    Page(button="December",
         underlyingTable=sundayTable,
         forwards=True,
         sortfunction=None,
         usereversed=False,
         onlyif=lambda x:x.date.isoformat()[4:8]=="-12-",
         hasDates=True),

]

for period in datePeriods:
    pages.append(Page(
         button=period,
         underlyingTable=allSongsTable,
         forwards=True,
         sortfunction=sortFunctionFromPeriod(period),
         usereversed=True,
         hasDates=False))
    pages.append(Page(
         button=period,
         underlyingTable=allSongsTable,
         forwards=False,
         sortfunction=sortFunctionFromPeriod(period),
         usereversed=False,
         hasDates=False))
if False:
    pages.append(
        Page(button="Test",
             underlyingTable=sundayTable,
             forwards=True,
             sortfunction=None,
             usereversed=True,
             hasDates=True)
        )
    
#                                                                    
#                                                                    
# __________________________ Output _________________________________
#                                                                    
#                                                                    
#                                                                    

def saveAs(output,filename):  # Save in all the outputprefixes locations
    for outputprefix in outputprefixes:
        with open(outputprefix+filename,"w") as f:
            print(output,file=f)
        print(filename)        

def serve_template(templatename, **kwargs):
    mytemplate = mylookup.get_template(templatename)
    return mytemplate.render(**kwargs)


def makepage(page):
    if page.usereversed:
        if page.sortfunction == None:
            finalTable =        filter(page.onlyif,reversed(page.underlyingTable))
        else:
            finalTable = reversed(sorted(filter(page.onlyif,page.underlyingTable),
                                         key=page.sortfunction))
    else:
        if page.sortfunction == None:
            finalTable =                 filter(page.onlyif,page.underlyingTable)
        else:
            finalTable =          sorted(filter(page.onlyif,page.underlyingTable),
                                         key=page.sortfunction)

    if page.hasDates:
        getSongDate = lambda song:song.date.isoformat()
        colourDateFunction = lambda song:colourDate(song.date)
    else:
        getSongDate = lambda song:""
        colourDateFunction = lambda song:""
            
    outputpage = serve_template(
        page.template,
        recentDates=recentDates,
        page=page,
        getSongDate=getSongDate,
        links=buttonLinks(page.button,page.forwards),
        finalTable=finalTable,
        colourDateFunction=colourDateFunction,
        bookNo=bookNo,
        bookColour=bookColour,
        makeID=makeID,
        colourFrequency=colourFrequency,
        today=today)

    for outputprefix in outputprefixes:
        with open(outputprefix+page.filename,"w") as f:
              print(outputpage,file=f)
        #print('\t\t'+outputprefix)
        print(page.filename)

def savehomepageas(outputfilename):
    homepage = serve_template("SeedfieldSongs.html",
                              links=buttonLinks("home",True),
                              linksOnHomepage=linksOnHomepage,
                              today=today)
    saveAs(homepage,outputfilename)
    

# ___________________________ MAIN _________________________

print('Do www() to save the website.')
def www():
    for filename in ["1SeedfieldSongs.html","index.html"]:
        savehomepageas(filename)                     
    for page in pages:
        makepage(page)
    print("Finished www.")

