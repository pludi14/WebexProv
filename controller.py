import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
import logging
from excelpkg.excel import Excelhandler
from webexapipkg.orgInformationen import OrgInformationen
from webexapipkg.webexAPIException import WebexAPIException
from webexapipkg.webexapi import Webexapi

from log.setup_logger import logger

logger=logging.getLogger("WP.controller")

class Controller():
    def __init__(self):
        self.__api=Webexapi()
        self.__excelhandler=None
        self.__excel_Daten=None
        self.__orgs=None   #Liste der Orgs
        self.__aktuelleOrg=None
        self.__prozessmax=0


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
            logger.info("__set_aktuelle_Org: Org ist nicht vorhanden.")
            raise WebexAPIException(text="__set_aktuelle_Org: Org nicht vorhanden.")
    def __get_aktuelle_Org(self): return self.__aktuelleOrg
    aktuelle_Org=property(__get_aktuelle_Org,__set_aktuelle_Org)


    def __orgsInitialisiert(self):
        if self.__orgs==None:
            return False
        else:
            return True
    org_Initialisiert = property(__orgsInitialisiert)


    def get_Progress(self):
        prozent=0
        if self.__excelhandler:
            if self.__prozessmax > 0:
                prozent=100/self.__prozessmax*self.__api.progress_User
        return prozent.__round__()

    def reset_Progress(self):
        self.__api.resetProgress()
        self.__prozessmax=0

    def leseExcel(self,exceldatei):
        self.__excelhandler=Excelhandler(self.__aktuelleOrg)
        self.__excelhandler.leseExcel(exceldatei)
        self.__excel_Daten=self.__excelhandler.getDaten()
        logger.info("Exceldatei eingelesen: %s", exceldatei)


    def starte_Prozess(self,update=False,insert=False,delete=False):
        update_user=[]
        insert_user=[]
        delete_user=[]
        responses={}
        responses["update"]=[]
        responses["insert"]=[]
        responses["delete"] = []
        self.__prozessmax=0
        for datensatz in self.__excel_Daten:

            if datensatz["doing"] == "update" and update == True:

                userid = self.__aktuelleOrg.org_Users[datensatz["emails"][0]]["id"]
                datensatz["id"]=userid
                update_user.append(datensatz)
                self.__prozessmax+=1
                logger.debug("User Update: " + datensatz["emails"][0])

            if datensatz["doing"] == "insert" and insert == True:
                insert_user.append(datensatz)
                self.__prozessmax += 1
                logger.debug("User Insert: %s",datensatz["emails"][0])

            if datensatz["doing"] == "update" and delete==True:
                userid = self.__aktuelleOrg.org_Users[datensatz["emails"][0]]["id"]
                datensatz["id"] = userid
                delete_user.append(datensatz)
                self.__prozessmax += 1
                logger.debug("User Delete: %s", datensatz["emails"][0])


        loop = asyncio.new_event_loop()
        if update:
            res = loop.run_until_complete(self.__user_Update(update_user))
            responses["update"]=res
        if insert:
            res=loop.run_until_complete(self.__user_Import(insert_user))
            responses["insert"]=res
        if delete:
            res = loop.run_until_complete(self.__user_Delete(delete_user))
            responses["delete"] = res
        loop.close()
        return responses


    async def __user_Update(self, userdaten):
        responses=[]
        with ThreadPoolExecutor(max_workers=10) as executor:  #Anzahl an gleichzeitiger Requests
            loop = asyncio.get_event_loop()
            futures = [
                loop.run_in_executor(executor, self.__api.updateUser, *(datensatz["id"],datensatz))
                for datensatz in userdaten
            ]
            for response in await asyncio.gather(*futures, return_exceptions=True):
                responses.append(response)

        return responses



    async def __user_Import(self, userdaten):
        responses = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            loop = asyncio.get_event_loop()
            futures = [
                loop.run_in_executor(executor, self.__api.insertUser, datensatz)

                for datensatz in userdaten
            ]
            for response in await asyncio.gather(*futures):
                responses.append(response)
        return responses

    async def __user_Delete(self, userdaten):
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

    def oauth(self, authcode):
        token=self.__api.getAccessToken(authcode)
        try:
            self.setToken(token)
            with open("Auth/token", "w") as file:
                file.write(token)
                file.close()
        except WebexAPIException as e:
            logger.info("Fehler: %s", e.kwargs["text"])

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





