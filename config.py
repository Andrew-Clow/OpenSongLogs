# __________ Input _________

prefix = "../../../Dropbox/Not work/Church Laptop Open Song Files/"
setpattern = "20*"
oldsetsglob = prefix + "sets2/" + setpattern
newsetsglob = prefix + "sets/"  + setpattern
songglob = prefix + "songs/*"
notnewpath = prefix + "sets/not new"
notsongspath = prefix + "sets/not songs"
includeAllSongsInSongHistoryTable = True

# __________ Dates _________

recentDays = {"three months":92,
              "six months":182.625,
              "year":365.25}

includeAllTimeInRecents = "All time"  # put emptystring if you don't want it

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

# __________ Output _________

outputprefixes =["./www/","../../../Dropbox/Not work/Sundays/SeedfieldSongs - sortable lists of songs we've sung/"]

makotemplates = "./templates"
makomodules = "./mako_modules"