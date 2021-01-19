from excelpkg.excel import Excelhandler
from webexapipkg.webexapi import Webexapi
from webexapipkg.orgInformationen import OrgInformationen
import asyncio


class Controller():
    def __init__(self):
        self.__api=Webexapi()
        self.__excelhandler=Excelhandler()
        self.__daten=None
        self.__orgs=[]

    def __getOrgs(self): return self.__orgs
    orgs=property(__getOrgs)


    def leseExcel(self,exceldatei):
        self.__excelhandler.leseExcel(exceldatei)
        self.__daten=self.__excelhandler.getDaten()


    def starteImport(self):
        if self.__daten:
            for datensatz in self.__daten:
                self.__api.insertUser(datensatz)

    def starteUpdate(self):
        return "Muss noch implentiert werden. controller.starteImport"



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
    apikey = "NmM3YTVjNzktMzAzZS00ZWI4LTg4ZWUtMzdjMjU1MDFhZTNlOWNiMzdkZGItZTRk_PF84_7d2b833a-567c-442f-be92-af5fb4c537be"
    ct=Controller()
    ct.setToken(apikey)


