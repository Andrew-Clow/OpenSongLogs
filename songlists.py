# Copyright 2019 Andrew Clow GPLv3 (see COPYING.txt)

import glob
import xml.etree.ElementTree as ElementTree
from collections import defaultdict
import os

import classes
import config
from thunk import *

# ____________________________________________________________________________________________________________________ #
#                      Song Replacements                                                                               #
# ____________________________________________________________________________________________________________________ #

"""
.d88888b                                 888888ba                    dP                                                           dP            
88.    "'                                88    `8b                   88                                                           88            
`Y88888b. .d8888b. 88d888b. .d8888b.    a88aaaa8P' .d8888b. 88d888b. 88 .d8888b. .d8888b. .d8888b. 88d8b.d8b. .d8888b. 88d888b. d8888P .d8888b. 
      `8b 88'  `88 88'  `88 88'  `88     88   `8b. 88ooood8 88'  `88 88 88'  `88 88'  `"" 88ooood8 88'`88'`88 88ooood8 88'  `88   88   Y8ooooo. 
d8'   .8P 88.  .88 88    88 88.  .88     88     88 88.  ... 88.  .88 88 88.  .88 88.  ... 88.  ... 88  88  88 88.  ... 88    88   88         88 
 Y88888P  `88888P' dP    dP `8888P88     dP     dP `88888P' 88Y888P' dP `88888P8 `88888P' `88888P' dP  dP  dP `88888P' dP    dP   dP   `88888P' 
                                 .88                        88                                                                                  
                             d8888P                         dP                                                                                  
"""

def LoadSongReplacements():
    from songreplacements import songreplacements
    return songreplacements

def LoadNeverReplace():
    from songreplacements import neverreplace
    return neverreplace

SongReplacements = Thunk(LoadSongReplacements, [], 'SongReplacements', info={'filesystem':'songreplacements.py'})
NeverReplace = Thunk(LoadNeverReplace, [], 'NeverReplace', info={'filesystem':'songreplacements.py'})

def ReturnMaybeReplace():
    def maybereplacesong(song):
        asong = SongReplacements.value.get(song,song)
#        if asong in NotSongs.value:           # cyclic dependency
#            print("You have a 'songreplacement' replacing a song with something that's listed in your 'not songs'.")
#            print("Why not just list the original in the 'not songs' set?")
#            print(song)
#            print(asong)
        return asong
    return maybereplacesong

MaybeReplaceSong = Thunk(ReturnMaybeReplace, [SongReplacements], 'MaybeReplaceSong')

# ____________________________________________________________________________________________________________________ #
#                      Song Files                                                                                      #
# ____________________________________________________________________________________________________________________ #

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

def rawSongsIn(pathtosongset):                                                     # Thunks: MaybeReplaceSong
   root = ElementTree.parse(pathtosongset).getroot()            #parse xml
   for sg in root.findall("slide_groups/slide_group"): #songs are slide groups
       if sg.get("type") == "song":                    #only songs
           yield MaybeReplaceSong.value(sg.get("name"))            #yield is return but makes an iterator rather than a standard funtion

NotSongs = Thunk(lambda: {song for song in rawSongsIn(config.notsongspath)}, [MaybeReplaceSong], name='NotSongs',
                 info={'filesystem':config.notsongspath})

OldSundaySetFilenames = Thunk(lambda :config.oldsetsglob,[],name='OldSundaySetFilenames',info={'filesystem':config.oldsetsglob})
SundaySetFilenames = Thunk(lambda :config.newsetsglob,[],name='SundaySetFilenames',info={'filesystem':config.newsetsglob})

def CalcSundayFileNames():
    sundayFiles = glob.glob(OldSundaySetFilenames.value)
    sundayFiles.extend(glob.glob(SundaySetFilenames.value))
    return sundayFiles
AllSundaySetFilenames = Thunk(CalcSundayFileNames, [OldSundaySetFilenames,SundaySetFilenames], name='AllSundaySetFilenames')

SongFileNames = Thunk(lambda: glob.glob(config.songglob), [], name='SongFileNames', info={'filesystem':config.songglob})

ActualSongFiles = Thunk(lambda:
                        [song for song in (os.path.basename(file)
                                           for file in SongFileNames.value)
                         if song not in NotSongs.value],
                        [SongFileNames, NotSongs], name='ActualSongFiles')

OKSongSet = Thunk(lambda :{MaybeReplaceSong.value(song) for song in ActualSongFiles.value}.difference(NotSongs.value),
                  [ActualSongFiles,MaybeReplaceSong], name='OKSongSet')

def CalculateSongListFromFilesWithReplacementsAndNoNotSongs():
    return list(sorted(OKSongSet.value))

OKSongList = Thunk(CalculateSongListFromFilesWithReplacementsAndNoNotSongs,
                   [OKSongSet], name='OKSongList')




# ____________________________________________________________________________________________________________________ #
#                      Sundays and Songs                                                                               #
# ____________________________________________________________________________________________________________________ #

"""
.d88888b                          dP                                 d8' .d88888b                                      
88.    "'                         88                                d8'  88.    "'                                     
`Y88888b. dP    dP 88d888b. .d888b88 .d8888b. dP    dP .d8888b.    d8'   `Y88888b. .d8888b. 88d888b. .d8888b. .d8888b. 
      `8b 88    88 88'  `88 88'  `88 88'  `88 88    88 Y8ooooo.   d8'          `8b 88'  `88 88'  `88 88'  `88 Y8ooooo. 
d8'   .8P 88.  .88 88    88 88.  .88 88.  .88 88.  .88       88  d8'     d8'   .8P 88.  .88 88    88 88.  .88       88 
 Y88888P  `88888P' dP    dP `88888P8 `88888P8 `8888P88 `88888P' 88        Y88888P  `88888P' dP    dP `8888P88 `88888P' 
                                                   .88                                                    .88          
                                               d8888P                                                 d8888P           
"""

def songsIn(pathtosongset):                                                     # Thunks: MaybeReplaceSong
   root = ElementTree.parse(pathtosongset).getroot()            #parse xml
   for sg in root.findall("slide_groups/slide_group"): #songs are slide groups
       if sg.get("type") == "song":                    #only songs
           name = MaybeReplaceSong.value(sg.get("name"))
           if name not in NotSongs.value:
               yield name            #yield is return but makes an iterator rather than a standard funtion

NotNew = Thunk(lambda: {song for song in songsIn(config.notnewpath)}, [MaybeReplaceSong], name='NotNew',
               info={'filesystem':config.notnewpath})

def CalculateSundaysAndSongs():

    sundays = defaultdict(list)
    songs = defaultdict(list)
    for song in OKSongList.value:
        songs[song]=[]
    used = set()

    for file in AllSundaySetFilenames.value:
        sunday = classes.getdate(os.path.basename(file))            #get date from filename
        for song in songsIn(file):
            sundays[sunday].append(song)            #this sunday we sang this song
            songs[song].append(sunday)              #we sang this song this sunday
            used.add(song)

    return sundays, songs, used

WhichSongsInWhichSundaySets = Thunk(CalculateSundaysAndSongs, [OKSongList, AllSundaySetFilenames], name='WhichSongsInWhichSundaySets',
                                    info={'slow':True})
SundaySongs = Thunk(lambda: WhichSongsInWhichSundaySets.value[0], [WhichSongsInWhichSundaySets], name='SundaySongs')
SongSundays = Thunk(lambda: WhichSongsInWhichSundaySets.value[1], [WhichSongsInWhichSundaySets], name='SongSundays')
UsedSongs = Thunk(lambda: WhichSongsInWhichSundaySets.value[2], [WhichSongsInWhichSundaySets], name='UsedSongs')

# ____________________________________________________________________________________________________________________ #
#                      PLain Song Lists                                                                                #
# ____________________________________________________________________________________________________________________ #

"""
 888888ba  dP          oo                                                    dP oo            dP            
 88    `8b 88                                                                88               88            
a88aaaa8P' 88 .d8888b. dP 88d888b.    .d8888b. .d8888b. 88d888b. .d8888b.    88 dP .d8888b. d8888P .d8888b. 
 88        88 88'  `88 88 88'  `88    Y8ooooo. 88'  `88 88'  `88 88'  `88    88 88 Y8ooooo.   88   Y8ooooo. 
 88        88 88.  .88 88 88    88          88 88.  .88 88    88 88.  .88    88 88       88   88         88 
 dP        dP `88888P8 dP dP    dP    `88888P' `88888P' dP    dP `8888P88    dP dP `88888P'   dP   `88888P' 
                                                                      .88                                   
                                                                  d8888P                                    
"""
SongsWithoutSongFiles = Thunk(lambda: [song for song in sorted(SongSundays.value)
                                       if song not in OKSongSet.value],
                              [OKSongList, SongSundays], name='SongsWithoutSongFiles')

def CheckForMissingSongs():
    if SongsWithoutSongFiles.value:
        print('_____________________ Missing songs report ____________________')
        print('   There are no actual song files for the following songs.     ')
        print('Please complete the lines below and save in songreplacements.py')
        for song in SongsWithoutSongFiles.value:
            print('"'+song+'":"",')
        print('_______________________________________________________________')
        print('You could run wwwlocal() and then open MissingSongs.html')
        print('______________ End of missing songs report ____________________')


AnyOldSongFiles = Thunk(lambda:
                        [song for song in (os.path.basename(file) for file in SongFileNames.value)],
                        [SongFileNames], name='AnyOldSongFiles')

SongsWithNumbers = Thunk(lambda:
                         [song for song in OKSongList.value if classes.hasNumber(song)],
                         [OKSongList], name='SongsWithNumbers')

SongsWithoutNumbers = Thunk(lambda:
                            [song for song in OKSongList.value if not classes.hasNumber(song)],
                            [OKSongList], name='SongsWithoutNumbers')


SongsUndealtWithWithoutNumbers = Thunk(lambda:
                                       [song for song in SongsWithoutNumbers.value
                                        if song not in NotSongs.value
                                        and song not in SongReplacements.value],
                                       [NotSongs, SongsWithoutNumbers], name='SongsUndealtWithWithoutNumbers')




# ____________________________________________________________________________________________________________________ #
#                      Song History Tables and Sunday Table                                                            #
# ____________________________________________________________________________________________________________________ #

"""
.d88888b                                dP       oo            dP                              
88.    "'                               88                     88                              
`Y88888b. .d8888b. 88d888b. .d8888b.    88d888b. dP .d8888b. d8888P .d8888b. 88d888b. dP    dP 
      `8b 88'  `88 88'  `88 88'  `88    88'  `88 88 Y8ooooo.   88   88'  `88 88'  `88 88    88 
d8'   .8P 88.  .88 88    88 88.  .88    88    88 88       88   88   88.  .88 88       88.  .88 
 Y88888P  `88888P' dP    dP `8888P88    dP    dP dP `88888P'   dP   `88888P' dP       `8888P88 
                                 .88                                                       .88 
                             d8888P                                                    d8888P  
"""

OurSongsTable = Thunk(lambda: [classes.SongHistory(song) for song in OKSongList.value if song in UsedSongs.value],
                      [SongSundays], name='OurSongsTable')

AllSongsTable = Thunk(lambda:[classes.SongHistory(song) for song in OKSongList.value],
                      [OKSongList, NotSongs, SongSundays], name='AllSongsTable')

def CalculateSundayTable():
    sundayTable = []
    for date in reversed(sorted(SundaySongs.value.keys())):
        sundayTable.extend([classes.SongOnDate(song, date) for song in SundaySongs.value[date]])
    return sundayTable

SundayTable = Thunk(CalculateSundayTable, [SundaySongs], name='SundayTable')

SongListFromSetsWithoutNumbers = Thunk(lambda:
                                       [song.songfilename for song in OurSongsTable.value if song.songnumber == ''],
                                       [OurSongsTable], name='SongListFromSetsWithoutNumbers')


# ____________________________________________________________________________________________________________________ #
#                      Song Contents                                                                                   #
# ____________________________________________________________________________________________________________________ #

"""
.d88888b                                 a88888b.                     dP                       dP            
88.    "'                               d8'   `88                     88                       88            
`Y88888b. .d8888b. 88d888b. .d8888b.    88        .d8888b. 88d888b. d8888P .d8888b. 88d888b. d8888P .d8888b. 
      `8b 88'  `88 88'  `88 88'  `88    88        88'  `88 88'  `88   88   88ooood8 88'  `88   88   Y8ooooo. 
d8'   .8P 88.  .88 88    88 88.  .88    Y8.   .88 88.  .88 88    88   88   88.  ... 88    88   88         88 
 Y88888P  `88888P' dP    dP `8888P88     Y88888P' `88888P' dP    dP   dP   `88888P' dP    dP   dP   `88888P' 
                                 .88                                                                         
                             d8888P                                                                          
"""

def blankSongContent():
    return classes.SongContent("blank", "blank", "blank")


def CalculateSongContents():
    songContents = defaultdict(blankSongContent)
    for file in SongFileNames.value:
        song = os.path.basename(file)
        songContents[song] = classes.SongContent(file)
    for song in SongsWithoutSongFiles.value:
        songContents[song]=classes.SongContent(song, song, "???\n<br>Sorry, no content.\n<br>???\n<br>If there were content for this song on disk,\n<br>it wouldn't be in this list!\n<br>???")
    return songContents

SongContents = Thunk(CalculateSongContents, [SongFileNames, SongsWithoutSongFiles], name='SongContents', info={'filesystem':config.songglob,'slow':True})


# ____________________________________________________________________________________________________________________ #
#                      Song Matches                                                                                    #
# ____________________________________________________________________________________________________________________ #

"""
.d88888b                                8888ba.88ba             dP            dP                         
88.    "'                               88  `8b  `8b            88            88                         
`Y88888b. .d8888b. 88d888b. .d8888b.    88   88   88 .d8888b. d8888P .d8888b. 88d888b. .d8888b. .d8888b. 
      `8b 88'  `88 88'  `88 88'  `88    88   88   88 88'  `88   88   88'  `"" 88'  `88 88ooood8 Y8ooooo. 
d8'   .8P 88.  .88 88    88 88.  .88    88   88   88 88.  .88   88   88.  ... 88    88 88.  ...       88 
 Y88888P  `88888P' dP    dP `8888P88    dP   dP   dP `88888P8   dP   `88888P' dP    dP `88888P' `88888P' 
                                 .88                                                                     
                             d8888P                                                                      
"""

def blankMatch():
    return classes.Match()

# TODO: This repeats the file access of the Sundays and Songs. Rewrite it.

def CalcMatches():

    # Matches from SongSets
    matches = defaultdict(blankMatch)

    for file in AllSundaySetFilenames.value:
        root = ElementTree.parse(file).getroot()            #parse xml
        for sg in root.findall("slide_groups/slide_group"): #songs are slide groups
            if sg.get("type") == "song":                    #only
                song = sg.get("name")
                matches[classes.songhash(song)].addFromSongSet(song, file)          #this sunday we sang this song

    # Matches from SongFileNames
    for file in SongFileNames.value:                              #Add songs that haven't been used
        sh=classes.songhash(os.path.basename(file))
        matches[sh].addFromSongFile(file)
    return [match for match in matches.values()
                if len(match.songfilenames) > 1]


Matches = Thunk(CalcMatches, [AllSundaySetFilenames, SongFileNames], name='Matches', info={'slow':True})

