# Copyright 2019 Andrew Clow GPLv3 (see COPYING.txt)

import PySimpleGUI as sg

import relativelocation
import where

justtesting=False
if not justtesting:
    from weboutput import listPages, homePages, songtextPages, privatePages, saveAuxFiles
else:
    # importing that stuff is very very slow at the moment. This bit is for justtesting the gui
    class S(object):
        def __init__(self,btn,pvt=False):
            self.button=btn
            self.content='Content of {0} page'.format(btn)
            self.private = pvt
            if '/' in btn:
                (dir,fname) = btn.split('/')
                self.location = relativelocation.RelativeLocation(dir+'/',btn+'.html')
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
        return ['jquery-currentversion.js','various.css','songtext/other.css','songtext/other.js']

    # end of justtesting bit




(listpageButtons,homepageButtons,songtextPageButtons,privatePageButtons) = \
     ([s.button for s in somepages.values()] for somepages in (listPages, homePages, songtextPages, privatePages))

leftcol = [
    [sg.Text('Song list pages')],
    [sg.Listbox(values=listpageButtons,
                default_values=listpageButtons,
                select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                size=(25,len(listpageButtons)),
                key='listpageButtons')],
    [sg.Button('Clear', key='Clear:listpageButtons')],  # ,sg.Button('All',key='All:listPages')],
    [],
    [sg.Text('Home pages')],
    [sg.Listbox(values=homepageButtons,
                default_values=homepageButtons,
                select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                size=(25,len(homepageButtons)),
                key='homepageButtons')],
    [sg.Button('Clear', key='Clear:homepageButtons')],  # ,sg.Button('All',key='All:listPages')],
]

middlecol = [
    [sg.Text('Song Text pages')],
    [sg.Listbox(values=songtextPageButtons,
                default_values=songtextPageButtons,
                select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                size=(25,len(songtextPageButtons)),
                key='songtextPageButtons')],
    [sg.Button('Clear',key='Clear:songtextPageButtons')],#,sg.Button('All',key='All:listPages')],
    [],
    [sg.Text('Private Pages')],
    [sg.Listbox(values=privatePageButtons,
                default_values=privatePageButtons,
                select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                size=(25, len(privatePageButtons)),
                key='privatePageButtons')],
    [sg.Button('Clear', key='Clear:privatePageButtons')],  # ,sg.Button('All',key='All:listPages')],

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
    for part,pagedict in partmeanings.items():
        for p in values[part]:
            places = pagedict[p].save(values['customoutputprefixes'])
            printmsg('{0} saved as {1} in'.format(p,pagedict[p].location.filename))
            for place in places:
                printmsg('\t'+place)
            # window.Element(part).SetValue(p)      # It'd be lovely if that worked, but it doesn't update the last one in each listbox.
    printmsg('Auxiliary files:')
    for place in saveAuxFiles(values['customoutputprefixes']):
        printmsg('\t'+place)
    printmsg('Done.')
    printmsg('_'*100)
    printmsg('')


while True:
    event, values = window.Read()
    if event is None or event == 'Exit':
        break
    elif event[0:6] == 'Clear:':
        window.Element(event[6:]).SetValue([])
    elif event == 'Generate webpages':
        savewith(values)


#    if event[0:6] == 'All:':
#        for b in listpageButtons:
#           window.Element(event[6:]).SetValue([b])         # I can't get this to work. .SetValue(listpageButtons) nor loop .SetValue(b)



window.Close()

