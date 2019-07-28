# Copyright 2019 Andrew Clow GPLv3 (see COPYING.txt)

def noneIsEmpty(thing):
    if thing:
        return thing
    else:
        return ''

class RelativeLocation(object):
    def __init__(self,subdir,filename):
        if subdir and not subdir[-1]=="/":
            raise ValueError('RelativeLocation.subdir must have a trailing slash (or be empty): '+subdir)
        if subdir and subdir[0]=="/":
            raise ValueError("RelativeLocation doesn't know how to handle root: "+subdir)
        self.subdir = subdir            # trailing slash please!
        self.filename = filename
        self.depth = 0 if not subdir else len([c for c in self.subdir if c=='/'])
        self.subdirNoSlash = '' if not subdir else subdir[0:-1]

    def __repr__(self):
        if self.subdir is None:
            return 'RelativeLocation(None,' + self.filename +'")'
        else:
            return 'RelativeLocation("' + self.subdir +'","'+ self.filename +'")'

    def within(self,prefix):              # INCLUDE trailing slash on prefix
        if not (prefix=='' or prefix[-1]=="/"):
            raise ValueError('RelativeLocation.within(prefix) must have a trailing slash (or be empty): '+prefix)
        return noneIsEmpty(prefix) + noneIsEmpty(self.subdir) + self.filename

    def pathto(self,location2):
        if self.subdir == location2.subdir:
            return location2.filename
        else:
            backtoroot = ''.join('../' * self.depth)  # go ../ as many times as we are currently deep
            return location2.within(backtoroot)

    def pathfrom(self,location1):
        return location1.pathto(self)

def directories2locations(directorydict):  # Flat, not recursive
    return [RelativeLocation(directory,file)
        for directory in directorydict.keys()
        for file in directorydict[directory]
    ]

"""
def test():
    this = RelativeLocation('here/there/', 'this.html')
    that = RelativeLocation('everywhere/', 'that.html')
    index = RelativeLocation(None, 'index.html')

    for thing in [
        this,
        that,
        'this to that:',
        this.pathto(that),
        'this from that:',
        this.pathfrom(that),
        'this from index:',this.pathfrom(index),
        'this to index:',this.pathto(index)]:
        print(thing)
    bad = RelativeLocation(None,'/usr/bin/root')
    print(bad)

test()

"""