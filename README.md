Copyright 2019 Andrew Clow GPLv3 (see COPYING.txt)

# OpenSongLogs

This python program works with the data produced by 
OpenSong [http://www.opensong.org/](http://www.opensong.org/)
to generate a website listing what song's you've used, when, and how often.

You can hopefully see ours at 
[https://seedfieldsongs.orgfree.com/](https://seedfieldsongs.orgfree.com/)

# Security

The stuff generated in the songtext folder includes song lyrics and 
should **not** be freely available on the internet without permission of 
the copyright holders, so you need to password protect that whole folder.

I used .htaccess and .htpasswd for that, but your web host may work differently.

## Setup

Make sure you create the output directories first.

You'll need to edit:

* `config.py` for setup - where OpenSong stores your files. 
  (I keep ours in Dropbox so it syncs between the church laptop and my own.)
* `where.py`  for website structure - output directories and filenames
* `songreplacements.py`  to rename old versions of songs to new versions.
   * The webpages in `wwwlocal/` are there to help you do this.
   * `SongComparison.html` is a good one to start with because it looks 
     for songs with almost identical names.
   * We use Songs Of Fellowship predominantly, but we didn't used to, 
     so I had a lot of old references in there.
* Make a set in OpenSong called `not songs` for ones you don't want 
  listed as songs. (We've got some liturgy and several versions of the 
  Lord's Prayer, and the Lord's Prayer for example completely skews the 
  usage data (and hence colouring system) by being used far more often 
  than any particular song.
* Make a set in OpenSong called `not new` for songs that you've used for 
  years and years that show up in your New lists because you haven't 
  used them recently.

I made a second OpenSong sets folder, called `sets2` where I store 
old song sets where it keeps them out of the way of current song sets.

We store all our song sets under filenames like `20190728` so they show up in order.
The program (`classes.py`) will need some editing if you use a different format.

## How to use it

Run `gui.py`.

There are two tabs - the first is so you say what you want generated. 
I've chosen the stuff that might change each week as the default and 
turned off the slowest to generate pages.

The second tab is for if you're re-running it after some changes - you 
tell it what changed on disk and it'll recalculate those bits of the pages
you ask for. (Sorry I haven't got it tracking changes 
to thousands of files in a few directories, and I'm not sure it should.)
Go back to the first tab when you're done in the second.

Until I've separated `where.py` and `songreplacements.py` and `config.py` 
out from the code, changes to these only take force when you recompile.
In particular, telling the program you changed `SongReplacements` or
`NeverReplace` isn't going to achieve anything, sorry, and you'll have to 
recompile/run from code. 

Note that it checks to see if it was going to change something in the webpages
before writing them. That means you might find that nothing happens because 
you didn't change anything.

## The python code

This is my first python program. 
Sorry if it's not very pythonesque!

As all of my programs and code, it's rather quirky and non-standard.

`Thunk` started off as a nice idea and got very messy. By contrast, 
`RelativeLocation` was a messy idea that turned out quite clean in practice.
Ho hum.

Throuhout the code, you'll come accross document-summary-visible headings using:

---

     .d888888                    oo oo     .d888888             dP      .8888b                                                                           
    d8'    88                             d8'    88             88      88   "                                                                           
    88aaaaa88a .d8888b. .d8888b. dP dP    88aaaaa88a 88d888b. d8888P    88aaa  88d888b. .d8888b. 88d8b.d8b.                                              
    88     88  Y8ooooo. 88'  `"" 88 88    88     88  88'  `88   88      88     88'  `88 88'  `88 88'`88'`88                                              
    88     88        88 88.  ... 88 88    88     88  88         88      88     88       88.  .88 88  88  88                                              
    88     88  `88888P' `88888P' dP dP    88     88  dP         dP      dP     dP       `88888P' dP  dP  dP                                              
                                                                                                                                                         
                                                                                                                                                         
    dP         dP     dP            dP      d8'      d8'                     dP                     oo dP                                            d8' 
    88         88     88            88     d8'      d8'                      88                        88                                           d8'  
    88d888b. d8888P d8888P 88d888b.       d8'      d8'   88d888b. .d8888b. d8888P .d8888b. 88d888b. dP 88  .dP     .d8888b. .d8888b. 88d8b.d8b.    d8'   
    88'  `88   88     88   88'  `88      d8'      d8'    88'  `88 88'  `88   88   88'  `88 88'  `88 88 88888"      88'  `"" 88'  `88 88'`88'`88   d8'    
    88    88   88     88   88.  .88 dP  d8'      d8'     88.  .88 88.  .88   88   88.  .88 88       88 88  `8b. dP 88.  ... 88.  .88 88  88  88  d8'     
    dP    dP   dP     dP   88Y888P' 88 88       88       88Y888P' `88888P8   dP   `88888P' dP       88 dP   `YP 88 `88888P' `88888P' dP  dP  dP 88       
                           88                            88                                         88                                                   
                           dP                            dP                                         dP                                                   

Ascii Art from 
http://patorjk.com/

http://patorjk.com/software/taag/#p=display&f=Nancyj&t=Ascii%20Art%20from%20%0Ahttp%3A%2F%2Fpatorjk.com%2F
