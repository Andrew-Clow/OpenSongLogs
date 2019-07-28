# Copyright 2019 Andrew Clow GPLv3 (see COPYING.txt)

import datetime as DT
import re
import xml.etree.ElementTree as ElementTree
import os
from collections import defaultdict

from songreplacements import songreplacements,neverreplace
from config import *
import songlists


# ______________________________________________________________________________________________________________________
#                   Dates
# ______________________________________________________________________________________________________________________

"""
888888ba             dP                     
88    `8b            88                     
88     88 .d8888b. d8888P .d8888b. .d8888b. 
88     88 88'  `88   88   88ooood8 Y8ooooo. 
88    .8P 88.  .88   88   88.  ...       88 
8888888P  `88888P8   dP   `88888P' `88888P' 
                                            
                                            
"""

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


# _____________________ Date ranges _______________________

class Dates(object):
    def __init__(self, datelist):
        self.dates = [d.isoformat() for d in reversed(sorted(datelist))]
        self.number = len(self.dates)

    def __str__(self):
        return "Dates(" + str(self.number) + ",[" + ", ".join(self.dates) + "])"

    def __repr__(self):
        return "Dates(" + str(self.number) + ",[" + ", ".join(self.dates) + "])"


def songNewOnDate(songfilename, date):
    if songfilename in songlists.notnew:
        return ""
    elif not songlists.songs[songfilename]:
        return "never"
    elif date == min(songlists.songs[songfilename]) and date > newnessStarts:
        return "new"
    else:
        return ""


def mapisoformat(alistoflists):
    return [[l.isoformat() for l in alist] for alist in alistoflists]


def justSince(listofdates, since):
    dates = [date for date in listofdates if date >= since]
    return Dates(dates)


recentPeriodMaximums = {period: 0 for period in recentDates}


def recentDatesOf(songfilename):  # updates recentPeriodMaximums as a side effect
    dates = songlists.songs[songfilename]
    recent = {}
    for period in datePeriods:
        recent[period] = justSince(dates, recentDates[period])
        howmany = recent[period].number
        if howmany > recentPeriodMaximums[period]:
            recentPeriodMaximums[period] = howmany
    return recent


# ______________________________________________________________________________________________________________________
#                      Colours
# ______________________________________________________________________________________________________________________

"""
 a88888b.          dP                                     
d8'   `88          88                                     
88        .d8888b. 88 .d8888b. dP    dP 88d888b. .d8888b. 
88        88'  `88 88 88'  `88 88    88 88'  `88 Y8ooooo. 
Y8.   .88 88.  .88 88 88.  .88 88.  .88 88             88 
 Y88888P' `88888P' dP `88888P' `88888P' dP       `88888P' 
                                                          
                                                          
"""


# ___________________ COLOURS _________________________
def colourDate(date):
    return dateColour.format(date.day*10)

def colourFrequency(period,freqs):
    no = freqs[period].number
    maxno = max(recentPeriodMaximums[period],1)
    lum = 100 - no / maxno * (100 - minLuminosity)  # 100 when no=0, minLuminosity when no=maxno
    return frequencyColour.format(int(round(lum)))  # eg hsl(135, 50%, 30%)


# ______________________________________________________________________________________________________________________
#                   Songs
# ______________________________________________________________________________________________________________________

"""
.d88888b                                      
88.    "'                                     
`Y88888b. .d8888b. 88d888b. .d8888b. .d8888b. 
      `8b 88'  `88 88'  `88 88'  `88 Y8ooooo. 
d8'   .8P 88.  .88 88    88 88.  .88       88 
 Y88888P  `88888P' dP    dP `8888P88 `88888P' 
                                 .88          
                             d8888P           
"""

def maybereplacesong(song):
    if song in songreplacements:
        return songreplacements[song]
    else:
        return song


# ________________________ Song Numbers ____________________

def vlookup(value, assoclist):
    answer = None
    for lowerbound in (sorted(assoclist.keys())):
        if value >= lowerbound:
            answer = assoclist[lowerbound]
    return answer


def bookNo(songnumber):
    if songnumber.isnumeric():
        return vlookup(int(songnumber), whichSoF) or ""
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
    def __init__(self, songfilename="Error:song filename not supplied"):
        self.songfilename = songfilename
        self.recentTimes = recentDatesOf(songfilename)
        m = songnumberNameRE.match(songfilename)
        if m:
            self.songnumber = m.group(1) or m.group(3)
            self.songtitle = m.group(2) or m.group(4)
        else:
            self.songnumber = ""
            self.songtitle = songfilename

#        selfsongnumber = songfilename[0:4]
#        if selfsongnumber.isdigit():
#            selfsongtitle = songfilename[5:]
#        else:
#            maybeHPmatch = hpRE.match(songfilename)
#            if maybeHPmatch:
#                selfsongnumber = maybeHPmatch.group(1)
#                selfsongtitle = maybeHPmatch.group(2)
#            else:
#                selfsongtitle = songfilename
#                selfsongnumber = ''
#        if not selfsongnumber == self.songnumber:
#            print(selfsongnumber + " " + self.songnumber)

    def __repr__(self):
        return ("SongHistory"
                + "(songfilename='" + self.songfilename
                + "',recentTimes=" + str(self.recentTimes)
                + ")")


class SongOnDate(SongHistory):
    def __init__(self,
                 songfilename="Error:song filename not supplied",  # Required
                 date="1970-01-01"):
        SongHistory.__init__(self, songfilename)
        if isinstance(date, DT.date):
            self.date = date
        else:
            self.date = getdate(date, "%Y-%m-%d")
        self.newToday = songNewOnDate(songfilename, self.date)

    def __repr__(self):
        return ("SongOnDate"
                + "(songfilename='" + self.songfilename
                + "',date='" + str(self.date)
                + "',newToday='" + self.newToday
                + "',recentTimes=" + str(self.recentTimes)
                + ")")

# ______________________________________________________________________________________________________________________
#                     Song Files
# ______________________________________________________________________________________________________________________

"""
.d88888b                                 88888888b oo dP                   
88.    "'                                88           88                   
`Y88888b. .d8888b. 88d888b. .d8888b.    a88aaaa    dP 88 .d8888b. .d8888b. 
      `8b 88'  `88 88'  `88 88'  `88     88        88 88 88ooood8 Y8ooooo. 
d8'   .8P 88.  .88 88    88 88.  .88     88        88 88 88.  ...       88 
 Y88888P  `88888P' dP    dP `8888P88     dP        dP dP `88888P' `88888P' 
                                 .88                                       
                             d8888P                                        
"""


hasNumberRE = re.compile("^\d\d\d\d |HP\d")


def hasNumber(asongname):
    return hasNumberRE.match(asongname)


# A SongContent is just a filename, a songname and some lyrics.
class SongContent(object):
    def __init__(self, file, songname="", lyrics=""):
        self.file = file
        if songname == "":
            self.songname = os.path.basename(file)
        else:
            self.songname = songname
        if lyrics == "":
            root = ElementTree.parse(file).getroot()
            self.lyrics = root.findtext("lyrics")
            if self.lyrics is None:
                self.lyrics = ""
            self.lyrics = re.sub("\n[.;][^\n]*", "", self.lyrics).replace("||", "\n").replace("\n", "\n<br>")
        else:
            self.lyrics = lyrics

    def hasNumber(self):
        return hasNumber(self.songname)

    def __str__(self):
        return 'SongFile("' + self.songname + '", "' + self.file + '", "' + self.lyrics + '")'

    def __repr__(self):
        return 'SongFile("' + self.songname + '", "' + self.file + '", "' + self.lyrics + '")'


# ______________________________________________________________________________________________________________________
#                      Hash Matches
# ______________________________________________________________________________________________________________________

"""
dP     dP                    dP                                dP            dP                         
88     88                    88                                88            88                         
88aaaaa88a .d8888b. .d8888b. 88d888b.    88d8b.d8b. .d8888b. d8888P .d8888b. 88d888b. .d8888b. .d8888b. 
88     88  88'  `88 Y8ooooo. 88'  `88    88'`88'`88 88'  `88   88   88'  `"" 88'  `88 88ooood8 Y8ooooo. 
88     88  88.  .88       88 88    88    88  88  88 88.  .88   88   88.  ... 88    88 88.  ...       88 
dP     dP  `88888P8 `88888P' dP    dP    dP  dP  dP `88888P8   dP   `88888P' dP    dP `88888P' `88888P' 
                                                                                                        
                                                                                                        
"""

def songhash(songtitle):
    it = re.sub('\(.*\)', '', songtitle.lower())  # Get rid of anything in brackets
    it = re.sub('[^a-z]', '', it)  # Convert to lowercase
    # and only keep letters
    return it



def numberless(asongname):
    songnumber = asongname[0:4]
    return not songnumber.isdigit()


# Matches keep track of songfiles and setfiles featuring possibly the same song:
partRE = re.compile("^\[(.*)\]")
notlyricsRE = re.compile("^[.;]|^\s*$")


def glarblyrics(lyrics):
    bit = ""
    verses = defaultdict(list)
    lyrics = lyrics.replace("||", "\n&nbsp;\n").replace("|", "\n")
    for line in lyrics.splitlines():
        ignorable = notlyricsRE.match(line)
        if not ignorable:
            newbit = partRE.match(line)
            if newbit:
                bit = newbit.group().upper()
                if bit == "[V]":
                    bit = "[V1]"
            else:
                verses[bit].append(line)
    return verses


def orders(anint):
    baselist = range(0, anint)
    lists = []
    for i in baselist:
        lists.append([i] + [x for x in baselist if not x == i])
    return lists


# A SongFile is just a songname, a filename and some structured lyrics.
class SongFile(object):
    def __init__(self, song, file, lyrics=""):
        self.song = song
        self.file = file
        self.lyrics = lyrics

    def __str__(self):
        return 'SongFile("' + self.song + '", "' + self.file + '", "' + self.lyrics + '")'

    def __repr__(self):
        return 'SongFile("' + self.song + '", "' + self.file + '", "' + self.lyrics + '")'

    def verses(self):
        if not self.lyrics:
            return None
        else:
            return glarblyrics(self.lyrics)


flatten = lambda l: [item for sublist in l for item in sublist]


class Match(object):
    def addNumberOf(self, asongname):
        songnumber = asongname[0:4]
        if songnumber.isdigit():
            self.sofNos.add(songnumber)

    def addFromSongFile(self, asongfilename):
        asongname = os.path.basename(asongfilename)
        if asongname not in songreplacements and asongname not in neverreplace:
            self.addNumberOf(asongname)
            root = ElementTree.parse(asongfilename).getroot()
            lyrics = root.findtext("lyrics")
            self.songfilenames.append(SongFile(asongname, asongfilename, lyrics))

    def addFromSongSet(self, asongname, asetfilename):
        self.addNumberOf(asongname)
        self.setfilenames.append(SongFile(asongname, asetfilename))

    def __init__(self,
                 asongfilename=None,  # Which may have come from a songfile
                 asetfilename=None
                ):  # or a Sunday songset.
        self.sofNos = set({})
        self.songfilenames = []
        self.setfilenames = []
        if asongfilename is not None:
            self.addFromSongFile(asongfilename)
        if asetfilename is not None and asongfilename is not None:
            self.addFromSongSet(asongfilename,asetfilename)

    def __repr__(self):
        return ("\nMatch(songfilenames=[\n"
                + ",\n".join(str(x) for x in self.songfilenames)
                + "\n], setfilenames=[\n"
                + ",\n".join(str(x) for x in self.setfilenames)
                + "\n], sofNos=set({"
                + "', '".join(self.sofNos)
                + "}))\n")

    def permutations(self):
        sfs = self.songfilenames
        tables = []
        verseses = [sf.verses() for sf in sfs]
        for apermutation in orders(len(sfs)):
            permutation = [apermutation[0]] + [i for i in apermutation[1:] if numberless(sfs[i].song)]
            if len(permutation) > 1:
                rows = defaultdict(list)
                rows["song"] = [sfs[i].song for i in permutation]
                verselist = verseses[0].keys()
                for verse in verselist:
                    rows[verse] = [verseses[i][verse] for i in permutation]
                rows["extras"] = [flatten(
                    [[v] + verseses[i][v] for v in verseses[i].keys() if not v in verselist]
                ) for i in permutation]
                if not any(rows["extras"]):
                    del rows["extras"]
                tables.append(rows)
        return tables

    def byebyefunction(self):
        if len(self.songfilenames) > 2:
            return "byebye"
        else:
            return "byebyetop"
