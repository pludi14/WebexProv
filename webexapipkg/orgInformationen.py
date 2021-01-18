from builtins import property


class OrgInformationen():
    def __init__(self, orgID, orgName):
        self.__lizenztypen={} # Dict mit Name der Lizenz=key + licenseID=value
        self.__anzahlFreieLizenzen=0 # Anzahl freie Lizenzen der Org
        self.__orgID=orgID
        self.__orgName=orgName
        self.__workspaces={}



    def __setAnzahlFreieLizenzen(self,x): self.__anzahlFreieLizenzen =x
    def __getAnzahlFreieLizenzen(self): return self.__anzahlFreieLizenzen
    anzahlFreieLizenzen=property(__getAnzahlFreieLizenzen,__setAnzahlFreieLizenzen)

    def __setLizenztypen(self,x): self.__lizenztypen =x
    def __getLizenztypen(self): return self.__lizenztypen
    lizenztypen=property(__getLizenztypen,__setLizenztypen)

    def __setWorkspaces(self,x): self.__workspaces =x
    def __getWorkspaces(self): return self.__workspaces
    workspaces=property(__getWorkspaces,__setWorkspaces)





