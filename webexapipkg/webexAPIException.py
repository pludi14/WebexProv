class WebexAPIException(Exception):

    def __init__(self, **kwargs):
        Exception.__init__(self)
        self.__kwargs = kwargs

    def __getKwargs(self): return self.__kwargs
    def __setKwargs(self,x): self.__kwargs=x
    kwargs=property(__getKwargs,__setKwargs)


