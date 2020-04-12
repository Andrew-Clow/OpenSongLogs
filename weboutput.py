# Copyright 2019 Andrew Clow GPLv3 (see COPYING.txt)

# Where the songlists.py and the mako templates meet to generate the output in places as specified by the where.py module.

from collections import defaultdict
from mako.lookup import TemplateLookup

import config
import songlists
import classes
import shutil
import where

from thunk import *

# __________________ CONFIGURATION _________________


mylookup = TemplateLookup(directories=[where.makotemplates],
                          module_directory=where.makomodules,
                          strict_undefined=True)

# ___________________ Sort orders by frequency ________________
# We'll multiply the frequencies by 10 to a power and sum.
# We use higher powers to emphasise that period above others in the sort order

powerDictDict = {"three months":
                     {"three months": 8,
                      "six months": 6,
                      "year": 4,
                      "four years": 2,
                      "All time": 0},
                 "six months":
                     {"three months": 6,
                      "six months": 8,
                      "year": 4,
                      "four years": 2,
                      "All time": 0},
                 "year":
                     {"three months": 4,
                      "six months": 6,
                      "year": 8,
                      "four years": 2,
                      "All time": 0},
                 "four years":
                     {"three months": 2,
                      "six months": 4,
                      "year": 6,
                      "four years": 8,
                      "All time": 0},
                 "All time":
                     {"three months": 0,
                      "six months": 2,
                      "year": 4,
                      "four years": 6,
                      "All time": 8}
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
def saveAs(output, location, customoutputprefixes = None):  # Save in all the outputprefixes locations
    myoutputprefixes = customoutputprefixes or where.outputprefixes
    for outputprefix in myoutputprefixes:
        with open(location.within(outputprefix), "r+b") as f:
            current = f.read()
            if current != output.encode('utf-8'):           # Test that it's genuinely a new version first.
                f.seek(0)
                f.write(output.encode('utf-8'))
                f.truncate()


def apply_template(templatename, **kwargs):
    mytemplate = mylookup.get_template(templatename)
    return mytemplate.render(**kwargs)



class Saveable(object):
    def __init__(self,
                 button,
                 contents,  # as a string Thunk
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
        saveAs(self.contents.value,self.location,myoutputprefixes)


# ______________________________________________________________________________________________________________________
#                         List Pages                                                                                   .
# ______________________________________________________________________________________________________________________

"""
.d88888b                                 888888ba                                      
88.    "'                                88    `8b                                     
`Y88888b. .d8888b. 88d888b. .d8888b.    a88aaaa8P' .d8888b. .d8888b. .d8888b. .d8888b. 
      `8b 88'  `88 88'  `88 88'  `88     88        88'  `88 88'  `88 88ooood8 Y8ooooo. 
d8'   .8P 88.  .88 88    88 88.  .88     88        88.  .88 88.  .88 88.  ...       88 
 Y88888P  `88888P' dP    dP `8888P88     dP        `88888P8 `8888P88 `88888P' `88888P' 
                                 .88                             .88                   
                             d8888P                          d8888P                    
"""
# The first type of Saveable page is a song page.
# It's atypical in that it doesn't have a presence in the site navigation,
# so it overrides some default methods of the Saveable class, sorry.

# BROKEN. :(

SongTemplate = Thunk(lambda:"SongTemplate.html", [],"SongTemplate", info={'filesystem':"SongTemplate.html"})

class SaveableSongPages(Saveable):
    def __init__(self):
        self.contents = songlists.SongContents
        super().__init__("Individual Song Pages", self.contents)

    def save(self,customoutputprefixes=None):
        myoutputprefixes = customoutputprefixes or where.outputprefixes
        actualSongContents = self.contents.value
        for s in actualSongContents:
            output = apply_template(SongTemplate.value,
                                    song = actualSongContents[s],
                                    bookNo=classes.bookNo,
                                    bookColour=config.bookColour,
                                    numberFromFileName=classes.numberFromFileName
            )
            saveAs(output,where.songlocation(s),myoutputprefixes)

individualSongPages = {'Individual Song Pages':SaveableSongPages()}



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
    def choosefinaltable():
        if page.usereversed:
            if page.sortfunction is None:
                return filter(page.onlyif, reversed(page.underlyingTable.value))
            else:
                return reversed(sorted(filter(page.onlyif, page.underlyingTable.value),
                                       key=page.sortfunction))
        else:
            if page.sortfunction is None:
                return filter(page.onlyif, page.underlyingTable.value)
            else:
                return sorted(filter(page.onlyif, page.underlyingTable.value),
                              key=page.sortfunction)

    finalTable = Thunk(choosefinaltable,[page.underlyingTable],page.button+'_finalTable')
    if page.hasDates:
        getSongDate = lambda song: song.date.isoformat()
        colourDateFunction = lambda song: classes.colourDate(song.date)
    else:
        getSongDate = lambda song: ""
        colourDateFunction = lambda song: ""

    outputpage = lambda:apply_template(
        page.template.value,
        recentDates=classes.recentDates,
        page=page,
        getSongDate=getSongDate,
        links=where.actualLinks(page.button),
        finalTable=finalTable.value,
        colourDateFunction=colourDateFunction,
        bookNo=classes.bookNo,
        bookColour=config.bookColour,
        isBackwards=where.isBackwards,
        colourFrequency=classes.colourFrequency,
        today=classes.today,
        songlocationforhref=where.songlocationforhref)
    return outputpage

ListPageTemplate = Thunk(lambda :"ListPageTemplate.html", [],'ListPageTemplate', info={'filesystem':"ListPageTemplate.html"})

class ListPage(Saveable):
    def __init__(self,
                 button,  # Use "Date" and "-Date" for the forwards and backwards versions
                 sortfunction,  # Lambda to return the field tuple to sort on
                 usereversed,  # Should we reverse after using the sortfunction?
                 hasDates,  # True to use SundayTable.value, false to put blanks in the New and Date columns
                 underlyingTable,  # Underlying table Thunk of SongHistory or SongOnDate
                 onlyif=lambda x: True,  # Lambda to keep records
                 template=ListPageTemplate,  # override if needed
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
                          contents = Thunk(makelistpage(self),[underlyingTable,template],name=button),
                          private = False
                          )

    def __repr__(self):
        return ("ListPage" +
                "(button='" + self.button +
                "',sortfunction=" + repr(self.sortfunction) +
                "',usereversed='" + repr(self.usereversed) +
                "',hasDates='" + repr(self.hasDates) +
                "',template=" + self.template.name +
                ",location='" + self.location +
                ")")


# Adding listPages:
# Make an entry here, and in the negateableButtons list.
# Probably add it into linksOnHomepage too.

listPages = {
    "Date":ListPage(button="Date",
                    underlyingTable=songlists.SundayTable,
                    sortfunction=None,
                    usereversed=False,
                    hasDates=True),
    "-Date":ListPage(button="-Date",
                     underlyingTable=songlists.SundayTable,
                     sortfunction=lambda x: x.date,  # Weirdly, this does the right thing
                     usereversed=False,  # when we don't reverse it
                     hasDates=True),
    "New":ListPage(button="New",
                   underlyingTable=songlists.SundayTable,
                   sortfunction=lambda x: (x.date, x.songfilename.lower()),
                   usereversed=True,
                   onlyif=lambda x: x.newToday.lower() == "new",
                   hasDates=True),
    "-New":ListPage(button="-New",
                    underlyingTable=songlists.SundayTable,
                    sortfunction=lambda x: (x.date, x.songfilename.lower()),
                    usereversed=False,
                    onlyif=lambda x: x.newToday.lower() == "new",
                    hasDates=True),
    "Song":ListPage(button="Song",
                    underlyingTable=songlists.AllSongsTable,
                    sortfunction=lambda x: x.songtitle.lower(),
                    usereversed=False,
                    hasDates=False),
    "-Song":ListPage(button="-Song",
                     underlyingTable=songlists.AllSongsTable,
                     sortfunction=lambda x: x.songtitle.lower(),
                     usereversed=True,
                     hasDates=False),
    "No.":ListPage(button="No.",
                   underlyingTable=songlists.AllSongsTable,
                   sortfunction=lambda x: x.songnumber + "zzzzzz" + x.songtitle.lower(),
                   usereversed=False,
                   hasDates=False),
    "-No.":ListPage(button="-No.",
                    underlyingTable=songlists.AllSongsTable,
                    sortfunction=lambda x: x.songnumber + "zzzzzz" + x.songtitle.lower(),
                    usereversed=True,
                    hasDates=False),
    "Non-SoF new":ListPage(button="Non-SoF new",
                           underlyingTable=songlists.SundayTable,
                           sortfunction=lambda x: (x.date, x.songfilename.lower()),
                           usereversed=True,
                           onlyif=lambda x: x.newToday.lower() == "new" and x.songnumber == '',
                           hasDates=True),
    "December":ListPage(button="December",
                        underlyingTable=songlists.SundayTable,
                        sortfunction=None,
                        usereversed=False,
                        onlyif=lambda x: x.date.isoformat()[4:8] == "-12-",
                        hasDates=True),
}

for period in classes.datePeriods:
    listPages.update({
        period:ListPage(
            button=period,
            underlyingTable=songlists.AllSongsTable,
            sortfunction=sortFunctionFromPeriod(period),
            onlyif=lambda song: song.recentTimes[period].number > 0,
            # BUG: I intended this to exclude songs not sung in that time period,
            # but it just excludes songs that haven't been sung at all.
            usereversed=True,
            hasDates=False),
    '-'+period:ListPage(
        button='-'+period,
        underlyingTable=songlists.AllSongsTable,
        sortfunction=sortFunctionFromPeriod(period),
        onlyif=lambda song: song.recentTimes[period].number > 0, # BUG as above.
        usereversed=False,
        hasDates=False)})
if None==3:
    TestPageTemplate = Thunk(lambda :"test.html", [],'TestPageTemplate', info={'filesystem':"test.html"})
    listPages.update({
        "Test":ListPage(button="Test",
                        template=TestPageTemplate.value,
                        underlyingTable=songlists.SundayTable,
                        sortfunction=None,
                        usereversed=True,
                        hasDates=True)
    })

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
HomePageTemplate = Thunk(lambda:"HomePageTemplate.html", [],"HomePageTemplate", info={'filesystem':"HomePageTemplate.html"})

homePages = {button:Saveable(button, pagecontent)
             for button in ["Home"] #["Seedfield Songs","Home"]
             for pagecontent in [Thunk(lambda:apply_template(HomePageTemplate.value,
                                                links=where.actualLinks("Home"),
                                                linksOnHomepage=where.linksOnHomepage,
                                                today=classes.today),{HomePageTemplate},button)]}



# ___________________________ MAIN _________________________





# ___________________________________________________________
# ______________________ Song Contents ______________________
# ___________________________________________________________

#  def outputTemplateInto(outputfilepath, templatename, **kwargs):
#    mytemplate = mylookup.get_template(templatename)
#    outputpage1 = mytemplate.render(**kwargs)
#    with open(outputfilepath, "w", encoding="utf-8") as f:
#        print(outputpage1, file=f)
#    print('output:\t' + songlists.os.path.basename(outputfilepath))


missingSongPretendSongfiles = defaultdict(songlists.blankSongContent)

SongSearchTemplate = Thunk(lambda :"SongSearchTemplate.html", [],'SongSearchTemplate', info={'filesystem':"SongSearchTemplate.html"})
SongTextHomepageTemplate = Thunk(lambda :"songtext.HomePageTemplate.html", [],'SongTextHomepageTemplate',
                                 info={'filesystem':"songtext.HomePageTemplate.html"})

songtextPages = {
    "Search":Saveable("Search",
                      Thunk(lambda:apply_template(SongSearchTemplate.value, songlist=songlists.OKSongList.value,
                            songContents=songlists.SongContents.value, numberFromFileName=classes.numberFromFileName,
                            pagetitle="Search the full text of songs", bookColour=config.bookColour,
                            bookNo=classes.bookNo),{SongSearchTemplate},"Search",info={'slow':True})),
    "Song Text Home":Saveable("Song Text Home",
                              Thunk(lambda:apply_template(SongTextHomepageTemplate.value,
                            links=where.actualLinks("Song Text Home"),
                            linksOnHomepage={"Search the text of all songs":"Search",
                                             "Main Home Page":"Home"},
                            today=classes.today),{SongTextHomepageTemplate},'Song Text Home'))
}

MatchSongsTemplate = Thunk(lambda :"MatchSongsTemplate.html", [],'MatchSongsTemplate', info={'filesystem':"MatchSongsTemplate.html"})
SongContentsTemplate = Thunk(lambda :"SongContentsTemplate.html", [],'SongContentsTemplate', info={'filesystem':"SongContentsTemplate.html"})
MatchSimilarSongnamesTemplate = Thunk(lambda :"MatchSimilarSongnamesTemplate.html", [],'MatchSimilarSongnamesTemplate',
                                      info={'filesystem':"MatchSimilarSongnamesTemplate.html"})

privatePages = {
    "Missing":Saveable("Missing",
                       Thunk(lambda :apply_template(MatchSongsTemplate.value,
                            fromsongs=songlists.SongsWithoutSongFiles.value,
                            tosongs=songlists.OKSongList.value,
                            songContents=dict(songlists.SongContents.value,
                                              **missingSongPretendSongfiles),
                            pagetitle="Missing songs: match up with actual songs and add to songreplacements.py"),
                   {MatchSongsTemplate},'Missing'),
                       private=True),

    "Numbered":Saveable("Numbered",
                        Thunk(lambda :apply_template(SongContentsTemplate.value,
                            songlist=songlists.SongsWithNumbers.value,
                            songContents=songlists.SongContents.value,
                            pagetitle="Song Content for all songs with numbers",
                            alter=lambda song: '"' + song + '",'),{SongContentsTemplate},'Numbered'),
                        private=True),
    "Numberless":Saveable("Numberless",
                          Thunk(lambda:apply_template(SongContentsTemplate.value,
                            songlist=songlists.SongListFromSetsWithoutNumbers.value,
                            songContents=songlists.SongContents.value,
                            pagetitle="Songs without numbers we've used",
                            alter=lambda song: '"' + song + '":'),{SongContentsTemplate},'Numberless'),
                          private=True),
    "Match Unnumbered":Saveable("Match Unnumbered",
                                Thunk(lambda :apply_template(MatchSongsTemplate.value,
                            fromsongs=songlists.SongListFromSetsWithoutNumbers.value,
                            tosongs=songlists.SongsWithNumbers.value,
                            songContents=songlists.SongContents.value,
                            pagetitle="Match up unnumbered songs"),{MatchSongsTemplate},'Match Unnumbered'),
                                private=True),
    "Undealt With":Saveable("Undealt With",
                            Thunk(lambda :apply_template(MatchSongsTemplate.value,
                            fromsongs=songlists.SongsUndealtWithWithoutNumbers.value,
                            tosongs=songlists.SongsWithNumbers.value,
                            songContents=songlists.SongContents.value,
                            pagetitle="Match up undealt with unnumbered songs"),{MatchSongsTemplate},'Undealt With'),
                            private=True),
    "Match Similar Songnames":Saveable("Match Similar Songnames",
                                       Thunk(lambda :apply_template("MatchSimilarSongnamesTemplate.html",
                            maybematches=songlists.Matches.value,
                            pagetitle="Match songs with similar Songnames"),{MatchSimilarSongnamesTemplate},'Match Similar Songnames'),
                                       private=True)
}



def www(customoutputprefixes=None):
    myoutputprefixes = customoutputprefixes or where.outputprefixes
    for homepage in homePages.values():
        homepage.save(myoutputprefixes)
    for page in listPages.values():
        page.save(myoutputprefixes)

def wwwlocal(customoutputprefixes=None):
    myoutputprefixes = customoutputprefixes or where.outputprefixes
    for pp in privatePages.values():
        pp.save(where.privateprefixes)
    for stp in songtextPages.values():
        stp.save(myoutputprefixes)

# ______________________________________________________________________________________________________________________
#                      Auxiliary files                                                                                 .
# ______________________________________________________________________________________________________________________



def saveAuxFiles(customoutputprefixes=None):
    myoutputprefixes = customoutputprefixes or where.outputprefixes
    for outputprefix in myoutputprefixes:
        yield (outputprefix+':')
        for location in where.publicAuxLocations:
            shutil.copy2(where.makotemplates + "/" + location.filename, location.within(outputprefix))
            yield('\t'+location.within(""))
    for outputprefix in where.privateprefixes:
        yield (outputprefix+':')
        for location in where.privateAuxLocations:
            shutil.copy2(where.makotemplates + "/" + location.filename, location.within(outputprefix))
            yield('\t'+location.within(""))

# ______________________________________________________________________________________________________________________
#                                                                                                                      .
# ______________________________________________________________________________________________________________________
