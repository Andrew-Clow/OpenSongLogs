# Copyright 2019 Andrew Clow GPLv3 (see COPYING.txt)


from mako.lookup import TemplateLookup

import config
import songlists
import classes
import shutil
import where

# __________________ CONFIGURATION _________________


mylookup = TemplateLookup(directories=[where.makotemplates],
                          module_directory=where.makomodules,
                          strict_undefined=True)

# ___________________ Sort orders by frequency ________________
# We'll multiply the frequencies by 10 to a power and sum.
# We use higher powers to emphasise that period above others in the sort order

powerDictDict = {"three months":
                     {"three months": 7,
                      "six months": 5,
                      "year": 3,
                      "All time": 0},
                 "six months":
                     {"three months": 5,
                      "six months": 7,
                      "year": 3,
                      "All time": 0},
                 "year":
                     {"three months": 3,
                      "six months": 5,
                      "year": 7,
                      "All time": 0},
                 "All time":
                     {"three months": 0,
                      "six months": 2,
                      "year": 4,
                      "All time": 6}
                 }

def sortFunctionFromPeriod(period):
    def sortFunction(song):
        total = 0
        for p in classes.datePeriods:
            total += (song.recentTimes[p].number
                      * 10 ** powerDictDict[period][p])
        return total

    return sortFunction



# _______________________ IDs ________________________

#def makeID(sometext):
#    return re.sub('[^A-Za-z0-9_-]', '', sometext) + 'ID'
    # Only keep alphanumeric or _ -


#
# ____________________________ PAGES ________________________________
#

# ______________________________________________________________________________________________________________________
#                Saveable                                                                                              .
# ______________________________________________________________________________________________________________________

"""

.d88888b                                      dP       dP          
88.    "'                                     88       88          
`Y88888b. .d8888b. dP   .dP .d8888b. .d8888b. 88d888b. 88 .d8888b. 
      `8b 88'  `88 88   d8' 88ooood8 88'  `88 88'  `88 88 88ooood8 
d8'   .8P 88.  .88 88 .88'  88.  ... 88.  .88 88.  .88 88 88.  ... 
 Y88888P  `88888P8 8888P'   `88888P' `88888P8 88Y8888' dP `88888P' 
                                                                   
"""
def saveAs(output, location,customoutputprefixes = None):  # Save in all the outputprefixes locations
    myoutputprefixes = customoutputprefixes or where.outputprefixes
    for outputprefix in myoutputprefixes:
        with open(location.within(outputprefix), "w", encoding="utf-8") as f:
            print(output, file=f)
        print(location.within(""))


def apply_template(templatename, **kwargs):
    mytemplate = mylookup.get_template(templatename)
    return mytemplate.render(**kwargs)


class Saveable(object):
    def __init__(self,
                 button,
                 contents,
                 private=False):
        self.button = button
        self.contents = contents
        self.private = private
        if private:
            self.location = where.privateButtonLocations[button]
        else:
            self.location = where.buttonLocations[button]

    def save(self,customoutputprefixes=None):
        myoutputprefixes = customoutputprefixes or where.outputprefixes
        if self.private:
            myoutputprefixes = where.privateprefixes
        saveAs(self.contents,self.location,myoutputprefixes)

# ______________________________________________________________________________________________________________________
#                         List Pages                                                                                   .
# ______________________________________________________________________________________________________________________

"""
dP        oo            dP       888888ba                                      
88                      88       88    `8b                                     
88        dP .d8888b. d8888P    a88aaaa8P' .d8888b. .d8888b. .d8888b. .d8888b. 
88        88 Y8ooooo.   88       88        88'  `88 88'  `88 88ooood8 Y8ooooo. 
88        88       88   88       88        88.  .88 88.  .88 88.  ...       88 
88888888P dP `88888P'   dP       dP        `88888P8 `8888P88 `88888P' `88888P' 
                                                         .88                   
                                                     d8888P                    
"""

def makelistpage(page):
    if page.usereversed:
        if page.sortfunction is None:
            finalTable = filter(page.onlyif, reversed(page.underlyingTable))
        else:
            finalTable = reversed(sorted(filter(page.onlyif, page.underlyingTable),
                                         key=page.sortfunction))
    else:
        if page.sortfunction is None:
            finalTable = filter(page.onlyif, page.underlyingTable)
        else:
            finalTable = sorted(filter(page.onlyif, page.underlyingTable),
                                key=page.sortfunction)

    if page.hasDates:
        getSongDate = lambda song: song.date.isoformat()
        colourDateFunction = lambda song: classes.colourDate(song.date)
    else:
        getSongDate = lambda song: ""
        colourDateFunction = lambda song: ""

    outputpage = apply_template(
        page.template,
        recentDates=classes.recentDates,
        page=page,
        getSongDate=getSongDate,
        links=where.actualLinks(page.button),
        finalTable=finalTable,
        colourDateFunction=colourDateFunction,
        bookNo=classes.bookNo,
        bookColour=config.bookColour,
        isBackwards=where.isBackwards,
        colourFrequency=classes.colourFrequency,
        today=classes.today)
    return outputpage

class ListPage(Saveable):
    def __init__(self,
                 button,  # Use "Date" and "-Date" for the forwards and backwards versions
                 sortfunction,  # Lambda to return the field tuple to sort on
                 usereversed,  # Should we reverse after using the sortfunction?
                 hasDates,  # True to use sundayTable, false to put blanks in the New and Date columns
                 underlyingTable,  # Underlying table of SongHistory or SongOnDate
                 onlyif=lambda x: True,  # Lambda to keep records
                 template="bydate.html",  # override if needed
                 ):
        self.button = button
        self.sortfunction = sortfunction
        self.usereversed = usereversed
        self.hasDates = hasDates
        self.template = template
        self.onlyif = onlyif
        self.underlyingTable = underlyingTable
        Saveable.__init__(self,
                          button   = button,
                          contents = makelistpage(self),
                          private = False
                          )

    def __repr__(self):
        return ("ListPage" +
                "(button='" + self.button +
                "',sortfunction=" + repr(self.sortfunction) +
                "',usereversed='" + repr(self.usereversed) +
                "',hasDates='" + repr(self.hasDates) +
                "',template='" + self.template +
                "',location='" + self.location +
                ")")


# Adding listPages:
# Make an entry here, and in the negateableButtons list.
# Probably add it into linksOnHomepage too.

listPages = [
    ListPage(button="Date",
             underlyingTable=songlists.sundayTable,
             sortfunction=None,
             usereversed=False,
             hasDates=True),
    ListPage(button="-Date",
             underlyingTable=songlists.sundayTable,
             sortfunction=lambda x: x.date,  # Weirdly, this does the right thing
             usereversed=False,  # when we don't reverse it
             hasDates=True),
    ListPage(button="New",
             underlyingTable=songlists.sundayTable,
             sortfunction=lambda x: (x.date, x.songfilename.lower()),
             usereversed=True,
             onlyif=lambda x: x.newToday.lower() == "new",
             hasDates=True),
    ListPage(button="-New",
             underlyingTable=songlists.sundayTable,
             sortfunction=lambda x: (x.date, x.songfilename.lower()),
             usereversed=False,
             onlyif=lambda x: x.newToday.lower() == "new",
             hasDates=True),
    ListPage(button="Song",
             underlyingTable=songlists.allSongsTable,
             sortfunction=lambda x: x.songtitle.lower(),
             usereversed=False,
             hasDates=False),
    ListPage(button="-Song",
             underlyingTable=songlists.allSongsTable,
             sortfunction=lambda x: x.songtitle.lower(),
             usereversed=True,
             hasDates=False),
    ListPage(button="No.",
             underlyingTable=songlists.allSongsTable,
             sortfunction=lambda x: x.songnumber + "zzzzzz" + x.songtitle.lower(),
             usereversed=False,
             hasDates=False),
    ListPage(button="-No.",
             underlyingTable=songlists.allSongsTable,
             sortfunction=lambda x: x.songnumber + "zzzzzz" + x.songtitle.lower(),
             usereversed=True,
             hasDates=False),
    ListPage(button="Non-SoF new",
             underlyingTable=songlists.sundayTable,
             sortfunction=lambda x: (x.date, x.songfilename.lower()),
             usereversed=True,
             onlyif=lambda x: x.newToday.lower() == "new" and x.songnumber == '',
             hasDates=True),
    ListPage(button="December",
             underlyingTable=songlists.sundayTable,
             sortfunction=None,
             usereversed=False,
             onlyif=lambda x: x.date.isoformat()[4:8] == "-12-",
             hasDates=True),

]

for period in classes.datePeriods:
    listPages.append(ListPage(
        button=period,
        underlyingTable=songlists.allSongsTable,
        sortfunction=sortFunctionFromPeriod(period),
        usereversed=True,
        hasDates=False))
    listPages.append(ListPage(
        button='-'+period,
        underlyingTable=songlists.allSongsTable,
        sortfunction=sortFunctionFromPeriod(period),
        usereversed=False,
        hasDates=False))
if None==3:
    listPages.append(
        ListPage(button="Test",
             template="test.html",
             underlyingTable=songlists.sundayTable,
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


"""
 .88888.    dP   dP                             888888ba                                      
d8'   `8b   88   88                             88    `8b                                     
88     88 d8888P 88d888b. .d8888b. 88d888b.    a88aaaa8P' .d8888b. .d8888b. .d8888b. .d8888b. 
88     88   88   88'  `88 88ooood8 88'  `88     88        88'  `88 88'  `88 88ooood8 Y8ooooo. 
Y8.   .8P   88   88    88 88.  ... 88           88        88.  .88 88.  .88 88.  ...       88 
 `8888P'    dP   dP    dP `88888P' dP           dP        `88888P8 `8888P88 `88888P' `88888P' 
                                                                        .88                   
                                                                    d8888P                    
"""


homepages = [Saveable(button,pagecontent)
             for button in ["Seedfield Songs","Home"]
             for pagecontent in [apply_template("SeedfieldSongs.html",
                                                links=where.actualLinks("Home"),
                                                linksOnHomepage=where.linksOnHomepage,
                                                today=classes.today)]]



# ___________________________ MAIN _________________________



print('Do www() to save the website.')

def www(customoutputprefixes=None):
    myoutputprefixes = customoutputprefixes or where.outputprefixes
    for homepage in homepages:
        homepage.save(myoutputprefixes)
    for page in listPages:
        page.save(myoutputprefixes)
    print("Finished www.")


# ___________________________________________________________
# ______________________ Song Contents ______________________
# ___________________________________________________________

#  def outputTemplateInto(outputfilepath, templatename, **kwargs):
#    mytemplate = mylookup.get_template(templatename)
#    outputpage1 = mytemplate.render(**kwargs)
#    with open(outputfilepath, "w", encoding="utf-8") as f:
#        print(outputpage1, file=f)
#    print('output:\t' + songlists.os.path.basename(outputfilepath))




songtextPages = [
    Saveable("Search",
             apply_template("SongSearch.html", songlist=songlists.songListApproved,
                            songContents=songlists.songContents, numberFromFileName=classes.numberFromFileName,
                            pagetitle="Search the full text of songs", bookColour=config.bookColour,
                            bookNo=classes.bookNo)),
    Saveable("Song Text Home",
             apply_template("songtext.index.html",
                            links=where.actualLinks("Song Text Home"),
                            linksOnHomepage={"Search the text of all songs":"Search",
                                             "Main Home Page":"Home"},
                            today=classes.today))
]
privatePages = [
    Saveable("Missing",
             apply_template("SongCompare.html",
                            fromsongs=songlists.songsWithoutSongFiles,
                            tosongs=songlists.songListFromFiles,
                            songContents=dict(songlists.songContents,
                                              **songlists.missingSongPretendSongfiles),
                            pagetitle="Missing songs: match up with actual songs and add to songreplacements.py"),
             private=True),

    Saveable("Numbered",
             apply_template("SongContent.html",
                            songlist=songlists.songsWithNumbers,
                            songContents=songlists.songContents,
                            pagetitle="Song Content for all songs with numbers",
                            alter=lambda song: '"' + song + '",'),
             private=True),
    Saveable("Numberless",
             apply_template("SongContent.html",
                            songlist=songlists.songListFromSetsWithoutNumbers,
                            songContents=songlists.songContents,
                            pagetitle="Songs without numbers we've used",
                            alter=lambda song: '"' + song + '":'),
             private=True),
    Saveable("Match Unnumbered",
             apply_template("SongCompare.html",
                            fromsongs=songlists.songListFromSetsWithoutNumbers,
                            tosongs=songlists.songsWithNumbers,
                            songContents=songlists.songContents,
                            pagetitle="Match up unnumbered songs"),
             private=True),
    Saveable("Undealt With",
             apply_template("SongCompare.html",
                            fromsongs=songlists.songsUndealtWithWithoutNumbers,
                            tosongs=songlists.songsWithNumbers,
                            songContents=songlists.songContents,
                            pagetitle="Match up undealt with unnumbered songs"),
             private=True),
    Saveable("Match Similar Songnames",
             apply_template("SongComparison.html", maybematches=songlists.maybematches),
             private=True)
]


print('Do wwwlocal() to save the local utils,')

def wwwlocal(customoutputprefixes=None):
    myoutputprefixes = customoutputprefixes or where.outputprefixes
    for pp in privatePages:
        pp.save(where.privateprefixes)
    for stp in songtextPages:
        stp.save(myoutputprefixes)

# ______________________________________________________________________________________________________________________
#                      Auxiliary files                                                                                 .
# ______________________________________________________________________________________________________________________




def saveAuxFiles(customoutputprefixes=None):
    myoutputprefixes = customoutputprefixes or where.outputprefixes
    for outputprefix in myoutputprefixes:
        for location in where.publicAuxLocations:
            shutil.copy2(where.makotemplates + "/" + location.filename, location.within(outputprefix))
            print(location.within(""))
    for outputprefix in where.privateprefixes:
        for location in where.privateAuxLocations:
            shutil.copy2(where.makotemplates + "/" + location.filename, location.within(outputprefix))
            print(location.within(""))

# ______________________________________________________________________________________________________________________
#                                                                                                                      .
# ______________________________________________________________________________________________________________________
