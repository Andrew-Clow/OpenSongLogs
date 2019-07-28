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
from songmatching import outputSongMatching
from recentsongs import (ourSongsTable,
                         notsongs,
                         songsWithoutSongFiles,
                         bookColour,
                         bookNo,
                         numberFromFileName)
print('\t\tCalculating local utils')





# _____________________SONG FILES__________________________

songFiles = glob.glob(songglob)


hasNumberRE = re.compile("^\d\d\d\d |HP\d")
def hasNumber(asongname):
    return hasNumberRE.match(asongname)





# A SongFile is just a filename, a songname and some lyrics.
class SongContent(object):
    def __init__(self,file,songname="",lyrics=""):
        self.file=file
        if songname=="":
            self.songname = os.path.basename(file)
        else:
            self.songname=songname
        if lyrics == "":
            root = ElementTree.parse(file).getroot()
            self.lyrics=root.findtext("lyrics")
            if self.lyrics==None:
                    self.lyrics = ""
            self.lyrics = re.sub("\n[\.;][^\n]*","",self.lyrics).replace("||","\n").replace("\n","\n<br>")
        else:
            self.lyrics=lyrics

    def hasNumber(self):
        return hasNumber(self.songname)

    def __str__(self):
        return ('SongFile("'+self.songname+'", "'+self.file+'", "'+self.lyrics+'")')
    def __repr__(self):
        return ('SongFile("'+self.songname+'", "'+self.file+'", "'+self.lyrics+'")')


    
def blankSongContent():
    return(SongContent("blank","blank","blank"))
songContents = defaultdict(blankSongContent)
for file in songFiles:
    song = os.path.basename(file) 
    songContents[song]=SongContent(file)
    
def maybereplacesong(song):
    if song in songreplacements:
        return songreplacements[song]
    else:
        return song
    
songListFromFiles = [song for song in(
                                 os.path.basename(file)
                                 for file in songFiles
                                  )]
songListApproved = [song for song in songListFromFiles
                    if song not in songreplacements.keys()]

songsWithNumbers = [song for song in songListFromFiles if hasNumber(song)]
songsWithoutNumbers = [song for song in songListFromFiles if not hasNumber(song)]

songListFromSetsWithoutNumbers = [song.songfilename
                                  for song in ourSongsTable
                                  if song.songnumber == '']

songsUndealtWithWithoutNumbers = [song for song in songsWithoutNumbers
                                  if song not in notsongs
                                  and song not in songreplacements.keys()]


missingSongPretendSongfiles = defaultdict(blankSongContent)
for song in songsWithoutSongFiles:
    songContents[song]=SongContent(song,song,"???\n<br>Sorry, no content.\n<br>???\n<br>If there were content for this song on disk,\n<br>it wouldn't be in this list!\n<br>???")


# _____________________________ OUTPUT ____________________________

mylookup = TemplateLookup(directories=["./templates"],
                          module_directory="./mako_modules",
                          strict_undefined=True)


def outputTemplateInto(templatename,outputfilepath,**kwargs):
    mytemplate = mylookup.get_template(templatename)
    outputpage1 = mytemplate.render(**kwargs)
    with open(outputfilepath,"w",encoding="utf-8") as f:
            print(outputpage1,file=f)
    print('output:\t'+os.path.basename(outputfilepath))

print('Do wwwlocal() to save the local utils,')
print('or wwwlocal("SongSearch","SongCompareUnumbered") for example, to just do some of them.')

def wwwlocal(whichones=None):
    if whichones == None or "SongComparison" in whichones:
        outputSongMatching()
    if whichones == None or "SongsWithoutNumbers" in whichones:
        outputTemplateInto("SongContent.html",
                       "./wwwlocal/SongsWithoutNumbers.html",
                       songlist=songListFromSetsWithoutNumbers,
                       songContents=songContents,
                       pagetitle="Songs without numbers we've used",
                       alter = lambda song:'"'+song+'":')
    if whichones == None or "SongContent" in whichones:
        outputTemplateInto("SongContent.html",
                       "./wwwlocal/SongContent.html",
                       songlist=songsWithNumbers,
                       songContents=songContents,
                       pagetitle="Song Content for all songs with numbers",
                       alter = lambda song:'"'+song+'",')
    if whichones == None or "SongComparison" in whichones:
        outputTemplateInto("SongCompare.html",
                       "./wwwlocal/SongCompareUnnumbered.html",
                       fromsongs=songListFromSetsWithoutNumbers,
                       tosongs=songsWithNumbers,
                       songContents=songContents,
                       pagetitle="Match up unnumbered songs"
                       )
    if whichones == None or "SongCompareUndealtWith" in whichones:
        outputTemplateInto("SongCompare.html",
                       "./wwwlocal/SongCompareUndealtWith.html",
                       fromsongs=songsUndealtWithWithoutNumbers,
                       tosongs=songsWithNumbers,
                       songContents=songContents,
                       pagetitle="Match up unnumbered songs"
                       )
    if whichones == None or "MissingSongs" in whichones:
        outputTemplateInto("SongCompare.html",
                       "./wwwlocal/MissingSongs.html",
                       fromsongs=songsWithoutSongFiles,
                       tosongs=songListFromFiles,
                       songContents=dict(songContents,**missingSongPretendSongfiles),
                       pagetitle="Missing songs: match up with actual songs and add to songreplacements.py"
                       )
    if whichones == None or "SongSearch" in whichones:
        outputTemplateInto("SongSearch.html",
                           "./wwwlocal/SongSearch.html",
                           songlist=songListApproved,
                           songContents=songContents,
                           numberFromFileName=numberFromFileName,
                           pagetitle="Search the full text of songs",
                           bookColour=bookColour,
                           bookNo=bookNo
                       )
        outputTemplateInto("SongSearch.html",
                           "D:/Andrew/Documents/Dropbox/Not work/Sundays/SeedfieldSongs - sortable lists of songs we've sung/SongSearch.html",
                           songlist=songListApproved,
                           songContents=songContents,
                           numberFromFileName=numberFromFileName,
                           pagetitle="Search the full text of songs",
                           bookColour=bookColour,
                           bookNo=bookNo
                       )
    
    print("Finished wwwlocal.")
def ss():wwwlocal("SongSearch")
