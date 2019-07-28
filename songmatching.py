import xml.etree.ElementTree as ElementTree
import datetime as DT
import os
import glob
import re
from collections import defaultdict
from mako.template import Template
from mako.lookup import TemplateLookup

from config import *
from songreplacements import songreplacements,neverreplace


def getdate(datestring,usingformat = filedateformat):
    datelen = len(DT.date.today().strftime(usingformat))        #how long this format is
    thedatestamp = DT.datetime.strptime(datestring[0:datelen],usingformat) #read the datelen prefix as a datetime
    thedate = DT.date(thedatestamp.year,thedatestamp.month,thedatestamp.day) #convert to a date
    return thedate

today = DT.date.today()
epoch = DT.date(1970,1,1)

# _____________________SONG FILES__________________________

sundayFiles = glob.glob(oldsetsglob)
sundayFiles.extend(glob.glob(newsetsglob))
songFiles = glob.glob(songglob)

# _____________________ Matches ___________________________

def songhash(songtitle):
    it = re.sub('\(.*\)','',songtitle.lower())  #Get rid of anything in brackets
    it = re.sub('[^a-z]', '', it)                 # Convert to lowercase
                                                    # and only keep letters
    return it
#    return re.sub('[^a-z]', '',songtitle.lower())


def numberless(asongname):
    songnumber = asongname[0:4]
    return not songnumber.isdigit()

    
# Matches keep track of songfiles and setfiles featuring possibly the same song:
partRE = re.compile("^\[(.*)\]")
notlyricsRE = re.compile("^[\.;]|^\s*$")
def glarblyrics(lyrics):
    bit=""
    verses=defaultdict(list)
    lyrics=lyrics.replace("||","\n&nbsp;\n").replace("|","\n")
    for line in lyrics.splitlines():
        ignorable=notlyricsRE.match(line)
        if not ignorable:
            newbit=partRE.match(line)
            if newbit:
                bit=newbit.group().upper()
                if bit=="[V]":
                    bit = "[V1]"
            else:
                verses[bit].append(line)
    return verses

def orders(anint):
    baselist = range(0,anint)
    lists = []
    for i in baselist:
        lists.append([i]+[x for x in baselist if not x==i])
    return lists


# A SongFile is just a songname, a filename and some lyrics.
class SongFile(object):
    def __init__(self,song,file,lyrics=""):
        self.song=song
        self.file=file
        self.lyrics=lyrics
    def __str__(self):
        return ('SongFile("'+self.song+'", "'+self.file+'", "'+self.lyrics+'")')
    def __repr__(self):
        return ('SongFile("'+self.song+'", "'+self.file+'", "'+self.lyrics+'")')
    def verses(self):
        if not self.lyrics:
            return None
        else:
            return glarblyrics(self.lyrics)

flatten = lambda l: [item for sublist in l for item in sublist]

class Match (object):
    def addNumberOf(self,asongname):
        songnumber = asongname[0:4]
        if songnumber.isdigit():
            self.sofNos.add(songnumber)
    
    def addFromSongFile(self,asongfilename):
        asongname = os.path.basename(asongfilename)
        if asongname not in songreplacements and asongname not in neverreplace:
            self.addNumberOf(asongname)
            root = ElementTree.parse(file).getroot()
            lyrics=root.findtext("lyrics")
            self.songfilenames.append(SongFile(asongname,asongfilename,lyrics))
        
    def addFromSongSet(self,asongname,asetfilename):
        self.addNumberOf(asongname)
        self.setfilenames.append(SongFile(asongname,asetfilename))
                    
    def __init__(self,
                 asongfilename=None,  # Which may have come from a songfile
                 asetfilename=None):  # or a Sunday songset.
        self.sofNos=set({})
        self.songfilenames=[]
        self.setfilenames=[]
        if asongfilename is not None:
            self.addFromSongFile(asongfilename)
        if asetfilename is not None:
            self.addFromSongSet(asetfilename)
    def __repr__(self):
        return ("\nMatch(songfilenames=[\n" 
                + ",\n".join(str(x) for x in self.songfilenames)
                + "\n], setfilenames=[\n"
                + ",\n".join(str(x) for x in self.setfilenames)
                + "\n], sofNos=set({"
                + "', '".join(self.sofNos)
                + "}))\n")

    def permutations(self):
        sfs=self.songfilenames
        tables=[]
        verseses=[sf.verses() for sf in sfs]
        for apermutation in orders(len(sfs)):
            permutation = [apermutation[0]]+[i for i in apermutation[1:] if numberless(sfs[i].song)]
            if len(permutation)>1:
                rows=defaultdict(list)
                rows["song"]=[sfs[i].song for i in permutation]
                verselist = verseses[0].keys()
                for verse in verselist:
                    rows[verse]=[verseses[i][verse] for i in permutation]
                rows["extras"]=[flatten(
                    [[v]+verseses[i][v] for v in verseses[i].keys() if not v in verselist]
                    )for i in permutation]
                if not any(rows["extras"]):
                    del rows["extras"]
                tables.append(rows)
        return tables

    def byebyefunction(self):
        if len(self.songfilenames) > 2:
            return "byebye"
        else:
            return "byebyetop"
    
def blankMatch():
    return Match()

# Matches from SongSets
matches = defaultdict(blankMatch)

for file in sundayFiles:
    root = ElementTree.parse(file).getroot()            #parse xml
    for sg in root.findall("slide_groups/slide_group"): #songs are slide groups
        if sg.get("type") == "song":                    #only 
            song = sg.get("name")
            matches[songhash(song)].addFromSongSet(song,file)          #this sunday we sang this song

# Matches from SongFiles
for file in songFiles:                              #Add songs that haven't been used
    sh=songhash(os.path.basename(file))
    matches[sh].addFromSongFile(file)

            
def glance(myDict):
    return dict([(key, myDict[key]) for key in sorted(myDict.keys())[:3]])
#print(glance(matches))


#print (matches["creationsingsthefatherssong"].songfilenames[0].verses())    

#print (matches["iamanewcreation"].permutations())    

maybematches = [ match for sh, match in matches.items()
                 if len(match.songfilenames)>1 ]





# __________________________ HTML output ____________________________


mylookup = TemplateLookup(directories=["./templates"],
                          module_directory="./mako_modules",
                          strict_undefined=True)

def serve_template(templatename, **kwargs):
    mytemplate = mylookup.get_template(templatename)
    return mytemplate.render(**kwargs)

outputpage = serve_template("SongComparison.html",maybematches=maybematches)

def outputSongMatching():
    print("matches: "+str(len(maybematches)))
    with open("./wwwlocal/SongComparison.html","w") as f:
        print(outputpage,file=f)
    print("SongComparison.html")


