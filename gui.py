# Copyright 2019 Andrew Clow GPLv3 (see COPYING.txt)

# The gui was created to allow me to specify a subset of the website to regenerate,
# but I had intended that it could go a second time when you tell it which things you'd changed,
# for example if you updated a template, it would be nice to not have to re-parse all the original data.
# Sadly it's not working fully effectively like that yet, but works for some things. Give it a go.

import PySimpleGUI as sg


import relativelocation
import where
import songlists
from thunk import *

justtesting=False
# ______________________________________________________________________________________________________________________
#                      Just testing                                                                                    .
# ______________________________________________________________________________________________________________________

if not justtesting:
    from weboutput import individualSongPages, listPages, homePages, songtextPages, privatePages, saveAuxFiles
else:
    # importing that stuff is very very slow at the moment. This bit is for justtesting the gui
    class S(object):
        def __init__(self,btn,pvt=False):
            self.button=btn
            self.content=Thunk(lambda:'Content of {0} page'.format(btn), set(), btn, info={'filesystem':btn+'_template.html'})
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
    individualSongPages = {'Individual Song Pages':S('lots of song pages')}

    def saveAuxFiles(outputprefixes):
        if outputprefixes == outputprefixes:
            return ['jquery-currentversion.js','various.css','songtext/other.css','songtext/other.js']

    # end of justtesting bit


# ______________________________________________________________________________________________________________________
#                      Tab 1                                                                                         .
# ______________________________________________________________________________________________________________________


(individualSongPageButtons,listpageButtons,homepageButtons,songtextPageButtons,privatePageButtons) = \
     ([s.button for s in somepages.values()] for somepages in (individualSongPages, listPages, homePages, songtextPages, privatePages))

buttonLists = {
    'listpageButtons':listpageButtons,
    'homepageButtons':homepageButtons,
    'songtextPageButtons':songtextPageButtons,
    'privatePageButtons':privatePageButtons,
    'individualSongPageButtons': individualSongPageButtons
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
                default_values=[],
                select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                size=(25,len(songtextPageButtons)),
                key='songtextPageButtons')],
    [sg.Button('Clear',key='Clear:songtextPageButtons'),sg.Button('All',key='All:songtextPageButtons')],
    [],
    [sg.Text('Private Pages')],
    [sg.Listbox(values=privatePageButtons,
                default_values=['Missing'],
                select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                size=(25, len(privatePageButtons)),
                key='privatePageButtons')],
    [sg.Button('Clear', key='Clear:privatePageButtons'),sg.Button('All',key='All:privatePageButtons')],
    [],
    [sg.Text('Individual Song Pages')],
    [sg.Listbox(values=individualSongPageButtons,
                default_values=[],
                select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                size=(25, len(individualSongPageButtons)),
                key='individualSongPageButtons')],
    [sg.Button('Clear', key='Clear:individualSongPageButtons'), sg.Button('All', key='All:individualSongPageButtons')],

]
def spacer(width,height=1):
    return sg.Text('',size=(width,height))

rightcol = [
    [sg.Button('Generate webpages'),
     sg.Text("Visit the 'Tell me what you changed...' \n tab before pressing this button again.",text_color='red',key='warning',visible=False)],
    [sg.Multiline(default_text='',size=(100,20),key='printmsg',autoscroll=True)]
]

tab1layout = [
    [sg.Frame('output to:',[[sg.Listbox(values=where.outputprefixes,
                                        default_values=where.outputprefixes[0:1],
                                        key='customoutputprefixes',
                                        select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                                        size=(max([len(loc) for loc in where.outputprefixes]),len(where.outputprefixes))
                                        )]])
     ],
    [sg.Column(leftcol),sg.Column(middlecol),sg.Column(rightcol)],
    [spacer(1)]
]

# ______________________________________________________________________________________________________________________
#                      Tab 2                                                                                 .
# ______________________________________________________________________________________________________________________


#tab2layout = [[sg.T('Yo.')]]

tablecontent = list(sorted([[thunk.name,thunk.info['filesystem']] for thunk in Thunk.Thunks if 'filesystem' in thunk.info]))
list.sort(tablecontent,key=lambda row:row[1])
tableheadings = ['Thing that changed','Files you may have changed                        ']

tab2layout = [
    [sg.Text('Select the things you changed:')],
    [sg.Text('Hold down ctrl or shift to selct more than one thing.')],
    [sg.Table(values=tablecontent, headings=tableheadings,
              select_mode=sg.TABLE_SELECT_MODE_EXTENDED,vertical_scroll_only=True,row_height=20,
                        auto_size_columns=True, justification='left', num_rows=len(tablecontent),
              alternating_row_color='#f5f5f5', key='thunks')],
    [sg.Button('Update')],
    [spacer(1)]
]

# ______________________________________________________________________________________________________________________
#                      Overall                                                                                 .
# ______________________________________________________________________________________________________________________

layout = [[sg.TabGroup([[sg.Tab(' Make website ', tab1layout), sg.Tab(' Tell me what you changed... ', tab2layout)]])]]

window = sg.Window('OpenSongLogs', layout)

# ______________________________________________________________________________________________________________________
#                      Handling tab 1                                                                                 .
# ______________________________________________________________________________________________________________________


partmeanings = {
    'individualSongPageButtons':individualSongPages,
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
    print('_'*100)

# ______________________________________________________________________________________________________________________
#                      Handling tab 2                                                                                 .
# ______________________________________________________________________________________________________________________

def updatethunks(indeces):
    thunknames = set()
    for i in indeces:
        thunkname = tablecontent[i][0]
        thunknames.add(thunkname)
        yield thunkname
    for thunk in Thunk.Thunks:
        if thunk.name in thunknames:
            thunk.unready_sinks()


# ______________________________________________________________________________________________________________________
#                      Main event loop                                                                                 .
# ______________________________________________________________________________________________________________________

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
        window.Element('warning').Update(visible=True)
    elif event == 'Update':
        if values['thunks']:
            window.Element('warning').Update(visible=False)
            thunknames = updatethunks(values['thunks'])
            sg.Popup('Updated:\n'+'\n'.join(thunknames)+'\n\nNow go back to the Make Website tab')
        else:
            sg.Popup('Please select at least one thing you changed first.')

window.Close()

