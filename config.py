# Copyright 2019 Andrew Clow GPLv3 (see COPYING.txt)

# This is the config file for where the input data is. See where.py for where the output goes.

# regex for finding assignment to function parameter that has a default value:
# def \w+\(.*(\w)+.*\):(.*\n)*.* \1 =
# assignment to a function parameter is a big mistake. function parameters that have a default value are implicitly static in python!



# __________ Input _________

inputprefix = "../../../Dropbox/Not work/Church/Church Laptop Open Song Files/"
setpattern = "20*"
oldsetsglob = inputprefix + "sets2/" + setpattern
newsetsglob = inputprefix + "sets/" + setpattern
songglob = inputprefix + "songs/*"
notnewpath = inputprefix + "sets/not new"
notsongspath = inputprefix + "sets/not songs"
includeAllSongsInSongHistoryTable = True

# __________ Dates _________

recentDays = {"three months":92,
#             "six months":182.625,
              "year":365.25,
	      "four years":1461}

includeAllTimeInRecents = "All time"  # put emptystring if you don't want it

datePeriods = list(recentDays.keys())
if includeAllTimeInRecents:
    datePeriods.append(includeAllTimeInRecents)

filedateformat = "%Y%m%d"
yearsAgoThatNewnessStarts = 5

# __________ Colours _________


dateColour = "hsl({}, 50%, 85%)" #include {} for where dayinmonth*10 goes
frequencyColour = "hsl(135, 50%, {}%)" #include {} for where luminosity goes
minLuminosity = 30

whichSoF = {1:1,
            641:2,
            1151:3,
            1691:4,
            2201:5,
            2711:6,
            3221:None}
bookColour = {1:"#cf7d7e",
              2:"#a385d5",
              3:"#5288c9",
              4:"#0e9d46",
              5:"#f9a654",
              6:"#b11b3b",
              "HP":"#375295",
              "":"",
              None:"",
              }
