# Todo

* Fix the way it generates stuff so that if you update on disk, 
  it reflects the new version, live. This means the second todo is now rather urgent: 
* Maybe add the feature of selectively recalculating lists. 
  Probably hard because we need an audit trail of dependencies.
  Actually, I'm probably going to end up with some form of lazy evaluation,
  but with message passing as to whether we need it again.
* Implement sorting via javascript rather than multiple pages. It's not 1998.
* Maybe add the feature of saving all lists to disk and reading at startup, 
  offering recalc as default or option thereof.
