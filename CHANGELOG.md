# 1.5.0

## Short urls, search and home buttons, icons

* There's a Search link and home button on all main pages.
* For songs with numbers you can type /song/1346 instead of /songtext/songs/1346 In Christ Alone and it'll redirect.
* In fact it'll redirect  /song/Awesome God  to  /songtext/songs/Awesome God.html  too. 
* Fontawesome icons


# 1.4.0 

## Individual Song Pages and check before rewriting

* Now the program generates a web page for each song in the SongContents list.
  There are links through from list pages. 
  I've yet to see how annoying that is when you're not signed in 
  and there's all these links you can't follow.
  Disadvantage: My ftp client dies after about 360 small transfers 
  and misses a lot of them out.
* Everything that's written using the SaveAs function in weboutput.py 
  is checked against the disk and if nothing's changed, nothing happens.
  This is the right thing to do to reduce upload traffic, 
  but may alarm you if you were expecting it to recalculate and it didn't.
* The pages sorting by how frequently songs have been sung now omit songs 
  that haven't been sung at all. 
  I intended it to exclude songs that haven't been sung within that 
  particular time period, but it's not worked out that way.


## 1.3.1 Bugfixes and tidy up of webpages

* Links between the homepage and song search pages.
* The entire song doesn't select any more when you click anywhere.

# 1.3.0

## Tell me what you changed and I'll recalculate your pages

There's a second tab now where you say what changed in the filesystem and 
the pages that you ask for back on the main pages will get recalculated
based on what you said changed. 

If you didn't say it changed, it won't recalculate. You could always quit 
and start the program again if you can't be bothered with this.

I find it handy for when I'm messing with a template etc.

# 1.2.2

## Faster startup times, faster for simple pages

Thanks to all the 1.2.1 hard work on the thunks front, the gui can load now
without calculating all the data for everything that might get saved.

If you just want to save the homepage, it won't take long. 

Still haven't got the recalc thing going yet, but nearer now.

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
