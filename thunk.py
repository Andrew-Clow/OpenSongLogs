import timeit

debug = 2

class Thunk(object):
    Thunks = [] # list of all thunks
    ReadyThunkNames = set() # set of thunks that are ready

    def __init__(self, calculate, sources, name, info=None):
        self.__calculate = calculate        # calculates the value
        self.sources = sources              # list of thunks on which this thunk is calculated
        self.__value = None
        self.sinks = []                     # list of thunks that use this one for propogating change downstream
        self.name = name
        self.info = info if info else {} # dictionary of info for whatever purpose you like - {'file':'template.html','slow':True} for example
        if debug >= 3:
            print("{0} is sourcing:".format(self.name))
        for source in sources:
            source.addsink(self)
            if debug >= 3:
                print("\t\t{1}.".format(self.name,source.name))
        Thunk.Thunks.append(self)

    @property
    def value(self):
        if self.name in Thunk.ReadyThunkNames:
            if debug >= 3:
                print(self.name+' already ready')
            return self.__value
        else:
            start_time = timeit.default_timer()
            if debug >= 2 or (debug==1 and self.info.get('slow',False)):
                print(self.name+' not ready. Calculating.')
                #throwerror()
            self.__value = self.__calculate()
            Thunk.ReadyThunkNames.add(self.name)
            elapsed = timeit.default_timer() - start_time
            if debug >= 2 or (debug==1 and self.info.get('slow',False)):
                print ('{0} ready in {1}.'.format(self.name,elapsed))
            return self.__value


    def unready_sinks(self):
        Thunk.ReadyThunkNames.discard(self.name)
        for s in self.sinks:
            s.unready_sinks()

    def unready_sources(self):
        Thunk.ReadyThunkNames.discard(self.name)
        for s in self.sources.values():
            s.unready_sources()

    @property
    def recalculate(self):                              # NEVER use in a loop. Make a Thunk including the list.
        self.unready_sources()                          # Tell ALL sources to recalculate!
        self.__value = self.__calculate()
        self.unready_sinks()                            # Tell ALL sinks they're not ready
        Thunk.ReadyThunkNames.add(self.name)
        return self.__value

    @property
    def recalculateall(self):
        self.__value = self.__calculate()
        Thunk.ReadyThunkNames.add(self.name)
        return self.__value

    def addsink(self,sink):
        self.sinks.append(sink)

    def addsinks(self,sinks):
        self.sinks.extend(sinks)
