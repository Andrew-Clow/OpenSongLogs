# Copyright 2019 Andrew Clow GPLv3 (see COPYING.txt)

# This module specifies where the webpages that are generated will end up.
# It also specifies what webpage buttons go to which webpages in the navigation and the gui.

import re
from relativelocation import *
import config

outputprefixes =["./www/","D:/Andrew/Documents/Dropbox/Not work/Church/Sundays/SeedfieldSongs - sortable lists of songs we've sung/"]
privateprefixes = ["./wwwlocal/"]
makotemplates = "./templates"
makomodules = "./mako_modules"

songtextsubdir = 'songtext/'
songssubdir = songtextsubdir + 'songs/'
def songlocation(song):
    return (RelativeLocation(songssubdir,song+".html"))
def songlocationforhref(song):
    return (songlocation(song).within(''))

publicAuxFilesNeeded = {
    songtextsubdir: [
        "comparisons.css",
        "favicon.ico",
        "jquery-3.4.1.js",
        "songcompare.js"
    ],
    "": [
        "jquery-3.4.1.js",
        "songlists.css",
    ]
}
privateAuxFilesNeeded = {
    "": [
        "comparisons.css",
        "favicon.ico",
        "jquery-3.4.1.js",
        "songcompare.js"
    ],
}

publicAuxLocations = directories2locations(publicAuxFilesNeeded)
privateAuxLocations = directories2locations(privateAuxFilesNeeded)
roothtaccess = RelativeLocation("","htaccess.txt")   # short urls for /sof/2643 Rename to .htaccess once you upload it.

# ______________________________________________________________________________________________________________________
#                       Buttons and Filenames
# ______________________________________________________________________________________________________________________

"""

 888888ba             dP     dP
 88    `8b            88     88
a88aaaa8P' dP    dP d8888P d8888P .d8888b. 88d888b. .d8888b.
 88   `8b. 88    88   88     88   88'  `88 88'  `88 Y8ooooo.
 88    .88 88.  .88   88     88   88.  .88 88    88       88
 88888888P `88888P'   dP     dP   `88888P' dP    dP `88888P'

"""

longSearchLinkText = "Search the full text of all songs"

linksOnHomepage = {"Most sung songs": "four years",
                   "Songs in date order": "Date",
                   "New songs": "New",
                   "New songs not in Songs of Fellowship": "Non-SoF new",
                   "Songs in name order": "Song",
                   "Songs in number order": "No.",
                   "Songs from December": "December",
                   longSearchLinkText:"Search"}

iconsOnHomepage = {"Most sung songs": "chart-bar",
                   "Songs in date order": "calendar-alt",
                   "New songs": "star",
                   "New songs not in Songs of Fellowship": "sun",
                   "Songs in name order": "sort-alpha-down",
                   "Songs in number order": "sort-numeric-down",
                   "Songs from December": "holly-berry",
                   longSearchLinkText:"search",
                   "Main Home Page":"home"}

negateableButtons = ["New",
               "Date",
               "Song",
               "No."]
negateableButtons.extend(config.datePeriods)


def indentifier(rawtext):
    return re.sub('[^A-Za-z0-9_-]', '_', rawtext)


buttonLocations = {}
for button in negateableButtons:
    buttonID = indentifier(button)
    buttonLocations.update({
        button:RelativeLocation('', "by_" + buttonID + ".html"),
        "-"+button:RelativeLocation('', "by_" + buttonID + "_backwards.html")
    })

buttonLocations.update({
    "Home":             RelativeLocation("", "index.html"),
#    "Seedfield Songs":  RelativeLocation("", "1SeedfieldSongs.html"),
    "Non-SoF new":      RelativeLocation("","by_Non-SoF_new.html"),
    "December":         RelativeLocation("","by_December.html"),
    "Test":             RelativeLocation("","test.html"),
    "Song Text Home":   RelativeLocation(songtextsubdir, "index.html"),
    "Search":           RelativeLocation(songtextsubdir, "SongSearch.html"),
    "Individual Song Pages":RelativeLocation(songssubdir,"(lots of individual files)"), # stub value just to fix my silly class hierarchy
    "Redirects": RelativeLocation("", "htaccess.txt"),

})
publicButtons = buttonLocations.keys()

privateButtonLocations = {
    'Missing':          RelativeLocation('','MissingSongs.html'),
    'Numbered':         RelativeLocation('','NumberedSongContents.html'),
    'Numberless':       RelativeLocation('','NumberlesssSongContents.html'),
    'Match Unnumbered': RelativeLocation('','MatchUnnumbered.html'),
    'Undealt With':     RelativeLocation('', 'MatchUndealtWith.html'),
    'Match Similar Songnames': RelativeLocation('', 'MatchSimilarSongnames.html')
}
privateButtons = privateButtonLocations.keys()

def outputfilename(button, forwards=True):
    if button[0]=="-":
        forwards = False
        button = button[1:]
    trunk = re.sub('[^A-Za-z0-9_-]', '_', button)
    if forwards:
        return "by_" + trunk + ".html"
    else:
        return "by_" + trunk + "_backwards.html"

def isForwards(button):
    return not button[0:1]=='-'

def isBackwards(button):
    return button[0:1]=='-'

def buttonText(frombutton):
    if frombutton[0:1]=='-':
        return frombutton[1:]
    else:
        return frombutton

def negateButton(button):               # only changes negateableButtons
    if button[0:1]=='-':
        return button[1:]
    elif button in negateableButtons:
        return '-' + button
    else:
        return button

def actualLinks(frombutton):
    myloc = buttonLocations[frombutton]
    links = {but:myloc.pathto(loc) for (but,loc) in buttonLocations.items() if isForwards(but)}
    links[buttonText(frombutton)]=myloc.pathto(buttonLocations[negateButton(frombutton)])
        # note that if frombutton is not in negateableButtons,
        # that's just links[frombutton]=buttonLocations[frombutton]
    return links

def printdict(d):
    for k,v in d.items():
        print ("{0}:\t{1}".format(k,v))

# for b in ["New","-New","Home"]:
#     print ("{0}\n{1}".format('-'*30,b))
#     printdict(actualLinks(b))

#def listButtonLinks(frombutton, forwards=True):
#    if isBackwards(frombutton):
#        forwards = False
#        frombutton = frombutton[1:]
#    links = {}
#    for tobutton in negateableButtons:
#        if tobutton == frombutton:
#            links[tobutton] = outputfilename(tobutton, not forwards)
#        else:
#            links[tobutton] = outputfilename(tobutton, True)
#    return links


