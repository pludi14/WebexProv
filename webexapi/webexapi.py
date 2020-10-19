import requests

class Webexapi():

    def __init__(self, key=""):
        self.__apikey = key


    def __setApikey(self, key=""): self.__apikey=key

    def insertUser(self,**kwargs):
        print("User anlegen muss noch implementiert werden")

