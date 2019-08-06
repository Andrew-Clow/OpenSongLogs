import timeit

debug = 0

class Thunk(object):
    Thunks = set() # set of all thunks
    ReadyThunkNames = set() # set of thunks that are ready

    # TODO: couldn't we use some sort of python introspection to get the name?

    def __init__(self, calculate, sources, name):
        self.sources = sources              # set of thunks on which this thunk is calculated
        self.__calculate = calculate        # calculates the value
        self.__value = None
        self.sinks = set()                     # set of thunks that use this one for propogating change downstream
        self.name = name
        if debug >= 2:
            print("{0} is sourcing:".format(self.name))
        for source in sources:
            source.addsink(self)
            if debug >= 2:
                print("\t\t{1}.".format(self.name,source.name))
        Thunk.Thunks.add(self)

    @property
    def value(self):
        if self.name in Thunk.ReadyThunkNames:
            if debug >= 2:
                print(self.name+' already ready')
            return self.__value
        else:
            start_time = timeit.default_timer()
            if debug:
                print(self.name+' not ready. Calculating.')
            self.__value = self.__calculate()
            Thunk.ReadyThunkNames.add(self.name)
            elapsed = timeit.default_timer() - start_time
            if debug:
                print ('{0} ready in {1}.'.format(self.name,elapsed))
            return self.__value


    def unready_sinks(self):
        Thunk.ReadyThunkNames.remove(self.name)
        for s in self.sinks:
            s.unready_sinks()

    def unready_sources(self):
        Thunk.ReadyThunkNames.remove(self.name)
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
        self.sinks.add(sink)

    def addsinks(self,sinks):
        self.sinks.update(sinks)
