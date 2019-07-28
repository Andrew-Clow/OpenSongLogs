Copyright 2019 Andrew Clow GPLv3 (see COPYING.txt)

OpenSongLogs

This python program works with the data produced by OpenSong http://www.opensong.org/
to generate a website listing what song's you've used, when, and how often.

You can hopefully see ours at http://seedfieldsongs.orgfree.com/

The stuff generated in the songtext folder includes song lyrics and should not be freely available on the internet without permission of the copyright holders, so you need to password protect that whole folder.

I used .htaccess and .htpasswd for that, but your web host may work differently.

Make sure you create the output directories first.

You'll need to edit:

 config.py for setup
 where.py  for website structure
 songreplacements.py  to rename old versions of songs to new versions.
                      The webpages in wwwlocal/ are there to help you do this.
                      SongComparison.html is a good one to start with because
                      it looks for songs with almost identical names.
                      We use Songs Of Fellowship predominantly, but we didn't used to,
                      so I had a lot of old references in there.

I made a second sets folder, called sets2 where I store old song sets.

We store all our song sets under filenames like 20190728 so they show up in order.
The program (classes.py) will need some editing if you use a different format.

This is my first python program. 
Sorry if it's not very pythonesque!

