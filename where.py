# Copyright 2019 Andrew Clow GPLv3 (see COPYING.txt)

import re
from relativelocation import *
import config

outputprefixes =["./www/","D:/Andrew/Documents/Dropbox/Not work/Sundays/SeedfieldSongs - sortable lists of songs we've sung/"]
privateprefixes = ["./wwwlocal/"]
makotemplates = "./templates"
makomodules = "./mako_modules"

songtextsubdir = 'songtext/'

publicAuxFilesNeeded = {
    songtextsubdir: [
        "comparisons.css",
        "favicon.ico",
        "jquery-3.4.1.js",
        "songcompare.js"
    ],
    "": [
        "jquery-3.4.1.js",
        "songlists.css"
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

linksOnHomepage = {"Date": "Date",
                   "Song": "Song",
                   "New": "New",
                   "Number": "No.",
                   "Most used": "All time",
                   "Non-SoF new": "Non-SoF new",
                   "December songs": "December"}

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
    "Seedfield Songs":  RelativeLocation("", "1SeedfieldSongs.html"),
    "Non-SoF new":      RelativeLocation("","by_Non-SoF_new.html"),
    "December":         RelativeLocation("","by_December.html"),
    "Test":             RelativeLocation("","test.html"),
    "Song Text Home":   RelativeLocation(songtextsubdir, "index.html"),
    "Search":           RelativeLocation(songtextsubdir, "SongSearch.html"),
})
publicButtons = buttonLocations.keys()

privateButtonLocations = {
    'Missing':          RelativeLocation('','MissingSongs.html'),
    'Numbered':         RelativeLocation('','SongContent.html'),
    'Numberless':       RelativeLocation('','SongsWithoutNumbers.html'),
    'Match Unnumbered': RelativeLocation('','SongCompareUnnumbered.html'),
    'Undealt With':     RelativeLocation('', 'SongCompareUndealtWith.html'),
    'Match Similar Songnames': RelativeLocation('', 'SongComparison.html')
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


