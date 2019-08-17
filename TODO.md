# Todo

* Move config and where and songreplacements into external data files 
  so that it can be a standalone executable.
* Some files are still being scanned at startup rather on page generation.
  This slows load times and means that you might need to say you changed 
  something if you did so in between starting up the program and generating
  pages.
* Implement sorting via javascript rather than multiple pages. It's not 1998.
* Put all the debug print output in some subwindow where it updates in a 
  live. Maybe even add a progress bar!
* Maybe add the feature of saving all lists to disk and reading at startup, 
  offering recalc as default or option thereof.
