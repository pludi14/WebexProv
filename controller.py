from excelpkg.excel import Excelhandler
from webexapipkg.webexapi import Webexapi
from webexapipkg.orgInformationen import OrgInformationen


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
        self.__getOrgInformations()

    def __getOrgInformations(self):

        orgIDs= self.__api.getOrgIDs()
        for org in orgIDs:
            orgInfo = OrgInformationen(org["id"],org["displayName"])
            orgLizenzen=self.__api.getLicenseFromOrg(org["id"])
            orgWorkspaces=self.__api.getWorkspaces(org["id"])
            orgInfo.lizenztypen=orgLizenzen
            orgInfo.workspaces=orgWorkspaces
            self.__orgs.append(orgInfo)



