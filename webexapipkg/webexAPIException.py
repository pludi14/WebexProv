class WebexAPIException(Exception):

    def __init__(self, **kwargs):
        Exception.__init__(self)
        self.__kwargs = kwargs

    def __getKwargs(self): return self.__kwargs
    def __setKwargs(self,x): self.__kwargs=x
    kwargs=property(__getKwargs,__setKwargs)

    def getMessage(self):
        text="Fehler: "+ str(self.__kwargs)
        if self.__kwargs["text"]:
            text=self.__kwargs["text"]
        return text




