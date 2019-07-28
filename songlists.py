# Copyright 2019 Andrew Clow GPLv3 (see COPYING.txt)

import glob
import xml.etree.ElementTree as ElementTree
from collections import defaultdict
import os

import classes
import config

# _____________________SONG FILES__________________________

sundayFiles = glob.glob(config.oldsetsglob)
sundayFiles.extend(glob.glob(config.newsetsglob))
songFiles = glob.glob(config.songglob)



# ___________________ Sundays and Songs ___________________

sundays = defaultdict(list)
songs = defaultdict(list)

def songsIn(pathtosongset):
   root = ElementTree.parse(pathtosongset).getroot()            #parse xml
   for sg in root.findall("slide_groups/slide_group"): #songs are slide groups
       if sg.get("type") == "song":                    #only songs
           songname = classes.maybereplacesong(sg.get("name"))
           yield classes.maybereplacesong(songname)            #yield is return but makes an iterator rather than a standard funtion

notnew   = [song for song in songsIn(config.notnewpath)]
notsongs = [song for song in songsIn(config.notsongspath)]

for file in sundayFiles:
    sunday = classes.getdate(os.path.basename(file))            #get date from filename
    for song in songsIn(file):
        if song not in notsongs:
            sundays[sunday].append(song)            #this sunday we sang this song
            songs[song].append(sunday)              #we sang this song this sunday


# ________________________ Tables ___________________________

actualSongFiles = [song for song in
                   (os.path.basename(file) for file in songFiles)
                   if song not in notsongs]

songListFromFiles = list(map(classes.maybereplacesong, actualSongFiles))

songsWithoutSongFiles = [song for song in sorted(songs)
                         if song not in songListFromFiles]

if songsWithoutSongFiles:
    print('_____________________ Missing songs report ____________________')
    print('   There are no actual song files for the following songs.     ')
    print('Please complete the lines below and save in songreplacements.py')
    for song in songsWithoutSongFiles:
        print('"'+song+'":"",')
    print('_______________________________________________________________')
    print('You could run wwwlocal() and then open MissingSongs.html')
    print('______________ End of missing songs report ____________________')



ourSongsTable = [classes.SongHistory(song) for song in sorted(songs)]
for song in songListFromFiles:                              #Add songs that haven't been used
    if not song in songs and song not in notsongs:
        songs[song]=[]
allSongsTable = [classes.SongHistory(song) for song in sorted(songs)]
sundayTable = []
for date in reversed(sorted(sundays.keys())):
    sundayTable.extend([classes.SongOnDate(song, date) for song in sundays[date]])

# _____________________ songContents __________________________

def blankSongContent():
    return classes.SongContent("blank", "blank", "blank")


songContents = defaultdict(blankSongContent)
for file in songFiles:
    song = os.path.basename(file)
    songContents[song] = classes.SongContent(file)



songListFromFiles = [song for song in(
                                 os.path.basename(file)
                                 for file in songFiles
                                  )]
songListApproved = [song for song in songListFromFiles
                    if song not in classes.songreplacements.keys()]

songsWithNumbers = [song for song in songListFromFiles if classes.hasNumber(song)]
songsWithoutNumbers = [song for song in songListFromFiles if not classes.hasNumber(song)]

songListFromSetsWithoutNumbers = [song.songfilename
                                  for song in ourSongsTable
                                  if song.songnumber == '']

songsUndealtWithWithoutNumbers = [song for song in songsWithoutNumbers
                                  if song not in notsongs
                                  and song not in classes.songreplacements.keys()]


missingSongPretendSongfiles = defaultdict(blankSongContent)
for song in songsWithoutSongFiles:
    songContents[song]=classes.SongContent(song, song, "???\n<br>Sorry, no content.\n<br>???\n<br>If there were content for this song on disk,\n<br>it wouldn't be in this list!\n<br>???")


# _____________ Hash Matches _______________


def blankMatch():
    return classes.Match()

# Matches from SongSets
matches = defaultdict(blankMatch)

for file in sundayFiles:
    root = ElementTree.parse(file).getroot()            #parse xml
    for sg in root.findall("slide_groups/slide_group"): #songs are slide groups
        if sg.get("type") == "song":                    #only
            song = sg.get("name")
            matches[classes.songhash(song)].addFromSongSet(song, file)          #this sunday we sang this song

# Matches from SongFiles
for file in songFiles:                              #Add songs that haven't been used
    sh=classes.songhash(os.path.basename(file))
    matches[sh].addFromSongFile(file)


maybematches = [ match for sh, match in matches.items()
                 if len(match.songfilenames)>1 ]
