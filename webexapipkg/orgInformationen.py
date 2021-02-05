from builtins import property


class OrgInformationen():
    def __init__(self, orgID, orgName):
        self.__lizenztypen={} # Dict mit Name der Lizenz=key + licenseID=value
        self.__anzahlFreieLizenzen=0 # Anzahl freie Lizenzen der Org
        self.__orgID=orgID
        self.__orgName=orgName
        self.__workspaces={}
        self.__messaging=""
        self.__meeting=""
        self.__org_Users=None


    def __setAnzahlFreieLizenzen(self,x): self.__anzahlFreieLizenzen =x
    def __getAnzahlFreieLizenzen(self): return self.__anzahlFreieLizenzen
    anzahlFreieLizenzen=property(__getAnzahlFreieLizenzen,__setAnzahlFreieLizenzen)

    def __setLizenztypen(self,x):
        #Lizenztypen werden gesetzt und die IDs den Variablen zugewiesen
        self.__lizenztypen =x
        self.__setLicenseTypes()
    def __getLizenztypen(self): return self.__lizenztypen
    lizenztypen=property(__getLizenztypen,__setLizenztypen)

    def __setWorkspaces(self,x): self.__workspaces =x
    def __getWorkspaces(self): return self.__workspaces
    workspaces=property(__getWorkspaces,__setWorkspaces)

    def __getMessaging_Lic_ID(self): return self.__messaging
    messaging_lic_ID=property(__getMessaging_Lic_ID)

    def __getMeeting_Lic_ID(self): return self.__meeting
    meeting_lic_ID=property(__getMeeting_Lic_ID)

    def __getOrg_ID(self): return self.__orgID
    org_ID=property(__getOrg_ID)

    def __getName(self): return self.__orgName
    org_Name=property(__getName)

    def __setOrg_Users(self,x): self.__org_Users =x
    def __getOrg_Users(self): return self.__org_Users
    org_Users=property(__getOrg_Users,__setOrg_Users)


    def __setLicenseTypes(self):
        #setzt die ID für die Lizenztypen
        for license in self.__lizenztypen:
            if license["name"]=="Messaging":
                self.__messaging=license["id"]
            if license["name"]=="Meeting - Webex Enterprise Edition":
                self.__meeting=license["id"]






