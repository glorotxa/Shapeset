import copy

class Curridata(object):
    
    def __init__(self, nfeatures, datagenerator, genparams, funclist, dependencies, funcparams = {}, batchsize = 1, seed
= 0):
    
        self.genparams = genparams
        self.batchsize = batchsize
        self.seed = seed
        self.nfeatures = nfeatures
        self.funclist = funclist
        self.dependencies = dependencies
        self.funcparams = funcparams
    
    
        self.__data = None
        self.__features = [None for i in range(self.nfeatures+1)]
    
        self.gen = datagenerator(**genparams)
        self.genit = self.gen.iterator(batchsize,seed)
    
    def _iterate(self):
        for i in self.genit:
            return i
    
    def next(self):
        self.__data = self._iterate()
        self.__data.update(self.funcparams)
        self.__features = [None for i in range(self.nfeatures+1)]
    
    def changegenparam(self,genparams):
        for t,u in genparams.iteritems():
            setattr(self.gen,t,u)
    
    
    # definition of the get property functions
    def _gettergen(i):
        def getter(self):
            if (self.__data is None):
                self.next()
            if not (self.__features[i] is None):
                return self.__features[i]
            else:
                if not(self.dependencies[i] is None):
                    tmp = copy.copy(self.__data)
                    for t,u in self.dependencies[i].iteritems():
                        self.getters[u](self)
                        tmp.update({t:self.__features[u]})
                    self.__features[i] = self.funclist[i](**(tmp))
                else:
                    self.__features[i] = self.funclist[i](**(self.__data))
            return self.__features[i]
        return getter
    
    #here you need to hard code the max features number and the targets and inputs property field
    __nbfeaturesmax = 10
    getters = [_gettergen(i) for i in range(__nbfeaturesmax)]
    image = property(getters[0])
    edges = property(getters[1])
    depth = property(getters[2])
    identity = property(getters[3])
    segmentation = property(getters[4])
    output = property(getters[5])
    edgesc = property(getters[6])
    