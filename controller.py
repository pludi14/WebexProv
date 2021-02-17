from concurrent.futures.thread import ThreadPoolExecutor
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
        self.__orgs=None   #Liste der Orgs
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
            orgUserResponse=self.__api.get_User(orgId=self.__aktuelleOrg.org_ID,max=999)
            orgUsers = {}
            for user in orgUserResponse:
                orgUsers[user["emails"][0]] = {"id":user["id"], "licenses":user["licenses"]}
            self.__aktuelleOrg.org_Users=orgUsers
        else:
            return "Org nicht vorhanden"
    def __get_aktuelle_Org(self): return self.__aktuelleOrg
    aktuelle_Org=property(__get_aktuelle_Org,__set_aktuelle_Org)


    def __orgsInitialisiert(self):
        if self.__orgs==None:
            return False
        else:
            return True
    org_Initialisiert = property(__orgsInitialisiert)


    def leseExcel(self,exceldatei):
        self.__excelhandler=Excelhandler(self.__aktuelleOrg)
        self.__excelhandler.leseExcel(exceldatei)
        self.__excel_Daten=self.__excelhandler.getDaten()



    def delete_User_Prozess(self):
        delete_user = []
        for datensatz in self.__excel_Daten:
            if datensatz["doing"] == "update":
                userid = self.__aktuelleOrg.org_Users[datensatz["emails"][0]]["id"]
                datensatz["id"]=userid
                delete_user.append(datensatz)
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.User_Delete(delete_user))
        loop.close()

    def starte_Prozess(self,update=False,insert=False,delete=False):

        update_user=[]
        inser_usert=[]

        for datensatz in self.__excel_Daten:
            if datensatz["doing"] == "update" and update == True:
                userid = self.__aktuelleOrg.org_Users[datensatz["emails"][0]]["id"]
                datensatz["id"]=userid
                update_user.append(datensatz)

            if datensatz["doing"] == "insert" and insert == True:
                inser_usert.append(datensatz)

        loop = asyncio.new_event_loop()
        if update:
            loop.run_until_complete(self.User_Update(update_user))
        if insert:
            loop.run_until_complete(self.User_Import(inser_usert))
        loop.close()


    async def User_Update(self, userdaten):
        with ThreadPoolExecutor(max_workers=10) as executor:  #Anzahl an gleichzeitiger Requests
            loop = asyncio.get_event_loop()
            futures = [
                loop.run_in_executor(executor, self.__api.updateUser, *(datensatz["id"],datensatz))
                for datensatz in userdaten
            ]
            for response in await asyncio.gather(*futures):
                print(response)


    async def User_Import(self,userdaten):
        with ThreadPoolExecutor(max_workers=10) as executor:
            loop = asyncio.get_event_loop()
            futures = [
                loop.run_in_executor(executor, self.__api.insertUser, datensatz)

                for datensatz in userdaten
            ]
            for response in await asyncio.gather(*futures):
                print(response)

    async def User_Delete(self,userdaten):
        with ThreadPoolExecutor(max_workers=10) as executor:
            loop = asyncio.get_event_loop()
            futures = [
                loop.run_in_executor(executor, self.__api.deleteUser, datensatz["id"])

                for datensatz in userdaten
            ]
            for response in await asyncio.gather(*futures):
                print(response)

    def orgReset(self):
        self.__aktuelleOrg=None
        self.__orgs=None


    def setToken(self, token):
        self.__api.apiToken=token
        asyncio.run(self.__getOrgInformations())
        #self.__getOrgInformations()


    async def __getOrgInformations(self):
        self.__orgs=[]
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



