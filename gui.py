# Copyright 2019 Andrew Clow GPLv3 (see COPYING.txt)

import PySimpleGUI as sg

import relativelocation
import where
import songlists
from thunk import *

justtesting=False
if not justtesting:
    from weboutput import listPages, homePages, songtextPages, privatePages, saveAuxFiles
else:
    # importing that stuff is very very slow at the moment. This bit is for justtesting the gui
    class S(object):
        def __init__(self,btn,pvt=False):
            self.button=btn
            self.content=Thunk(lambda:'Content of {0} page'.format(btn),set(),btn)
            self.private = pvt
            if '/' in btn:
                (d,f) = btn.split('/')
                self.location = relativelocation.RelativeLocation(d+'/',btn+'.html')
            else:
                self.location = relativelocation.RelativeLocation('',btn+'.html')
        def save(self,customoutputprefixes=None):
            if self.private:
                ops = ['private place 1']
            else:
                ops = customoutputprefixes or ["standard place 1","standard place 2"]
            for o in ops:
                yield o

    listPages = {'New':S('New'),'Date':S('Date'),'No.':S('No.'),'Freq.':S('Freq.')}
    homePages = {'Home':S('Home'),'SFS':S('SFS')}
    songtextPages = {'songtext/SongSearch':S('songtext/SongSearch'),'songtext/index':S('songtext/index')}
    privatePages = {'SongMatch':S('SongMatch',True),'SongComparison':S('SongComparison',True),'SongCompare':S('SongCompare',True)}

    def saveAuxFiles(outputprefixes):
        if outputprefixes == outputprefixes:
            return ['jquery-currentversion.js','various.css','songtext/other.css','songtext/other.js']

    # end of justtesting bit




(listpageButtons,homepageButtons,songtextPageButtons,privatePageButtons) = \
     ([s.button for s in somepages.values()] for somepages in (listPages, homePages, songtextPages, privatePages))

buttonLists = {
    'listpageButtons':listpageButtons,
    'homepageButtons':homepageButtons,
    'songtextPageButtons':songtextPageButtons,
    'privatePageButtons':privatePageButtons
}

leftcol = [
    [sg.Text('Song list pages')],
    [sg.Listbox(values=listpageButtons,
                default_values=listpageButtons,
                select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                size=(25,len(listpageButtons)),
                key='listpageButtons')],
    [sg.Button('Clear', key='Clear:listpageButtons'),sg.Button('All',key='All:listpageButtons')],
    [],
    [sg.Text('Home pages')],
    [sg.Listbox(values=homepageButtons,
                default_values=homepageButtons,
                select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                size=(25,len(homepageButtons)),
                key='homepageButtons')],
    [sg.Button('Clear', key='Clear:homepageButtons'),sg.Button('All',key='All:homepageButtons')],
]

middlecol = [
    [sg.Text('Song Text pages')],
    [sg.Listbox(values=songtextPageButtons,
                default_values=songtextPageButtons,
                select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                size=(25,len(songtextPageButtons)),
                key='songtextPageButtons')],
    [sg.Button('Clear',key='Clear:songtextPageButtons'),sg.Button('All',key='All:songtextPageButtons')],
    [],
    [sg.Text('Private Pages')],
    [sg.Listbox(values=privatePageButtons,
                default_values=privatePageButtons,
                select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                size=(25, len(privatePageButtons)),
                key='privatePageButtons')],
    [sg.Button('Clear', key='Clear:privatePageButtons'),sg.Button('All',key='All:privatePageButtons')],

]
def spacer(width,height=1):
    return sg.Text('',size=(width,height))

rightcol = [
    [sg.Button('Generate webpages')],
    [sg.Multiline(default_text='',size=(100,20),key='printmsg',autoscroll=True)]
]

layout = [
    [sg.Frame('output to:',[[sg.Listbox(values=where.outputprefixes,
                                        default_values=where.outputprefixes,
                                        key='customoutputprefixes',
                                        select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                                        size=(max([len(loc) for loc in where.outputprefixes]),len(where.outputprefixes))
                                        )]])
     ],
    [sg.Column(leftcol),sg.Column(middlecol),sg.Column(rightcol)],
    [spacer(1)]
]


window = sg.Window('OpenSongLogs', layout)

partmeanings = {
    'listpageButtons':listPages,
    'songtextPageButtons':songtextPages,
    'privatePageButtons':privatePages,
    'homepageButtons':homePages
}

def printmsg(msg):
    window.Element('printmsg').Update(window.Element('printmsg').Get()+msg)

def savewith(values):
    printmsg('Saving non-private pages in:')
    for place in values['customoutputprefixes']:
        printmsg('\t'+place)
    for part,pagedict in partmeanings.items():
        for p in values[part]:
            pagedict[p].save(values['customoutputprefixes'])
            printmsg('{0} saved as \n\t{1}'.format(p,pagedict[p].location.filename))
            # window.Element(part).SetValue(p)      # It'd be lovely if that worked, but it doesn't update the last one in each listbox.
                                                    # Ah, no SetValue(elt) turns it on, so this turns them on in sequence ending with the last.
                                                    # You can SetValue(remainingItemsList) if you like.
    printmsg('Auxiliary files:')
    for place in saveAuxFiles(values['customoutputprefixes']):
        printmsg('\t'+place)
    printmsg('Done.')
    printmsg('_'*100)
    printmsg('')


#window.Show()
songlists.CheckForMissingSongs()    # TODO: make this a GUI thing!
while True:
    event, values = window.Read()
    if event is None or event == 'Exit':
        break
    elif event[0:6] == 'Clear:':
        window.Element(event[6:]).SetValue([])
    elif event[0:4] == 'All:':
        window.Element(event[4:]).SetValue(buttonLists[event[4:]])
    elif event == 'Generate webpages':
        savewith(values)



window.Close()

