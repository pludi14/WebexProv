from excelpkg.excel import Excelhandler
from webexapipkg.webexapi import Webexapi
from webexapipkg.orgInformationen import OrgInformationen
from webexapipkg.webexAPIException import WebexAPIException
import asyncio


class Controller():
    def __init__(self):
        self.__api=Webexapi()
        self.__excelhandler=None
        self.__excel_Daten=None
        self.__orgs=[]
        self.__aktuelleOrg=None

    def __getOrgs(self): return self.__orgs
    orgs=property(__getOrgs)

    def __set_aktuelle_Org(self,id):
        # Hier wird die aktuell ausgewählte Org gesetzt. Prüfun gob OrgID vorhanden ist
        # + Aller User der Org in Dict self.__aktuelleOrgUserIDs geladen.
        orgVorhanden=False
        aktuelleOrg=None
        for org in self.__orgs:
            if org.org_ID==id:
                aktuelleOrg = org
                orgVorhanden=True
        if orgVorhanden:
            self.__aktuelleOrg=aktuelleOrg
            orgUserResponse=self.__api.get_User(orgId=self.__aktuelleOrg.org_ID)
            orgUsers = {}
            for user in orgUserResponse:
                orgUsers[user["emails"][0]] = {"id":user["id"], "licenses":user["licenses"]}
            self.__aktuelleOrg.org_Users=orgUsers
        else:
            return "Org nicht vorhanden"
    def __get_aktuelle_Org(self): return self.__aktuelleOrg
    aktuelle_Org=property(__get_aktuelle_Org,__set_aktuelle_Org)


    def leseExcel(self,exceldatei):
        self.__excelhandler=Excelhandler(self.__aktuelleOrg)
        self.__excelhandler.leseExcel(exceldatei)
        self.__excel_Daten=self.__excelhandler.getDaten()


    def starteImport(self):
        if self.__excel_Daten:
            for datensatz in self.__excel_Daten:
                self.__api.insertUser(datensatz)

    def starte_Update(self):

            if self.__excel_Daten:
                for datensatz in self.__excel_Daten:
                    try:
                        userid=self.__aktuelleOrg.org_Users[datensatz["emails"][0]]["id"]
                        self.__api.updateUser(userid,datensatz)
                    except WebexAPIException as e:
                        print("Fehler: " + e.kwargs["text"])






    def setToken(self, token):
        self.__api.apiToken=token
        asyncio.run(self.__getOrgInformations())
        #self.__getOrgInformations()


    async def __getOrgInformations(self):

        orgIDs= self.__api.getOrgIDs()
        for org in orgIDs:
            orgInfo = OrgInformationen(org["id"],org["displayName"])
            infos = asyncio.gather(self.__api.getLicenseFromOrg(org["id"]), self.__api.getWorkspaces(org["id"])) #Asyncio Task einrichten
            await infos #warten bis task vorbei. Beide Methoden werden gleichzeitig durchgeführt.
            orgInfo.lizenztypen=infos.result()[0]
            orgInfo.workspaces=infos.result()[1]
            self.__orgs.append(orgInfo)



if __name__ == '__main__':
    None



