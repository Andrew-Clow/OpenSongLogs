# 1.2.1

## Thunks

A thunk is a promised value that's calculated when it's first needed,
then stored for subsequent use. Google lazy evaluation.

Anyway, I've called them thunks because I couldn't think of a better name.
My thunks can be told to recalculate. At this point, I'm not using that 
functionality, but this was a big rewrite, so I'm committing at this point
and bumping the version number a bit.

# 1.2.0

## GUI is here!

* The GUI lets you only save some places. Unfortunately at the moment, 
  if you change something and press the button again, it'll save exactly
  the same content again. This is a massive bug, but hey, it looks pretty.
* Renamed some templates.
* Fixed some bugs in the private pages where I hadn't realised they relied on jquery.

# 1.1.0

## Refactored, reorganised etc

Wow, well that was a biggie!

* Split off website structure into where.py
* RelativeLocation helps calculate relative addresses for links
* gui is currently just a stub, don't get excited yet
* Reorganised so that individual pages and destinations can be done at will (which was needed before the gui can be useful
* Unified generation of lists of songs into songlists.py and generation of webpages into weboutput.py
* Now publishing full text search into songtext/SongSearch.html but **you should get yourself password protection on that subdirectory!** I used .htaccess and .htpasswd but of course they
re not in the repo! 

---

# 1.0.0

## Initial commit
