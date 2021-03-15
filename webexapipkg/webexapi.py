import requests
from webexapipkg.webexAPIException import WebexAPIException
import json
import os
import pathlib
import logging
from log.setup_logger import logger
from http.client import HTTPConnection

class Webexapi():

    def __init__(self, apikey=""):
        self.__apiToken = apikey
        self.__path = pathlib.Path(__file__).parent.absolute()
        self.__workdir = pathlib.Path().absolute()
        self.__progess_User=0
        self.__authUrl = "https://webexapis.com/v1/access_token"
        self.__clientID = "C945b60582f59d9ebd4c9aa664b316f17f0ca4c85794252b54395bb5ac49fe408"
        self.__secretID = "f2b3951e610b279bcae0e3dcfc0306627d171873cda6ce018313916d51ccb860"
        self.__redirectURI = "http://localhost:5000/auth"



    logger = logging.getLogger("WB.webexapi")

    # logging from urllib3 to console
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)
    # print statements from `http.client.HTTPConnection` to console/stdout
    # Auf 1 setzen für Debug
    HTTPConnection.debuglevel = 0



    def __setApiToken(self, x): self.__apiToken =x
    def __getApiToken(self): return self.__apiToken
    apiToken=property(__getApiToken, __setApiToken)

    def __get_Progress_User(self): return self.__progess_User
    progress_User=property(__get_Progress_User)



    def __createRequest(self, urlZiel, methode, queryParameter={}, querryData="", header=""):
        apiUrl = "https://webexapis.com/v1/"+urlZiel
        if header:
            httpHeaders = header
        else:
            httpHeaders = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.__apiToken}


        if methode=="GET":
            response = requests.get(url=apiUrl, headers=httpHeaders, params=queryParameter)

        if methode=="PUT":
            response = requests.put(url=apiUrl, headers=httpHeaders, params=queryParameter, data=querryData)

        if methode=="POST":
            response = requests.post(url=apiUrl, headers=httpHeaders, params=queryParameter, data=querryData)

        if methode=="DELETE":
            response = requests.delete(url=apiUrl, headers=httpHeaders, params=queryParameter)

            #responsetext = json.loads(response.text)
            print(response.text)

        if response.status_code == 200:
            #logger.debug(str(responsetext))
            responsetext = json.loads(response.text)
            return responsetext

        if response.status_code == 204:
            logger.debug("Response Code 204: Kein Content.")

        else:
            logger.debug("createRequest Fehler: "+ str(response.status_code) + " " + response.text)
            raise WebexAPIException(statuscode=response.status_code, text=response.text)


    def get_User(self, **kwargs):
        queryParams = kwargs if kwargs else {}
        response=self.__createRequest("people", "GET", queryParams)
        return response["items"]

    def insertUser(self, daten):
        data = daten
        # queryParams = {"callingData:" "true"}
        jsondata = json.dumps(data)
        response = self.__createRequest("people", "POST", querryData=jsondata)
        self.__progess_User = self.__progess_User + 1
        return response


    def deleteUser(self, personID):
        response = self.__createRequest("people/"+personID, "DELETE")
        self.__progess_User=self.__progess_User+1
        return response


    def updateUser(self, personid ,daten):
        personID = personid
        #data = {}
        #for key in kwargs:
        #    data[key]=kwargs[key]
        #queryParams = {"callingData:" "true"}
        jsondata=json.dumps(daten)
        response = self.__createRequest("people/"+personID, "PUT", querryData=jsondata)
        self.__progess_User=self.__progess_User+1

        return response

    def getOrgIDs(self):
        response = self.__createRequest("organizations", "GET")
        return response["items"]

    async def getLicenseFromOrg(self, orgID=""):
        querryParams={}
        querryParams["orgId"]=orgID
        response=self.__createRequest("licenses", "GET", queryParameter=querryParams)
        return response["items"]

    def insertDevice(self, placeID):
        querryParams={}
        querryParams["placeId"]=placeID
        response=self.__createRequest("devices/activaionCode","POST",queryParameter=querryParams)
        #return activationCode

    async def getWorkspaces(self,orgID=""):
        querryParams = {}
        querryParams["orgId"] = orgID
        response = self.__createRequest("workspaces", "GET", queryParameter=querryParams)
        return response["items"]

    def getAccessToken(self, authcode):

        payload = ("grant_type=authorization_code&client_id={0}&client_secret={1}&"
                   "code={2}&redirect_uri={3}").format(self.__clientID, self.__secretID, authcode, self.__redirectURI)
        headers = {'accept': 'application/json', 'content-type': 'application/x-www-form-urlencoded', }
        response=self.__createRequest("access_token", "POST", querryData=payload, header=headers)
        return response["access_token"]


    def resetProgress(self):
        self.__progess_User=0


if __name__=="__main__":
    api=Webexapi(apikey="ZmVhN2NhODItMmRkYi00OWQ1LThlMjAtNmQxMWE5N2Y3ZDBjN2MwNDc1NGItMmVm_PF84_7d2b833a-567c-442f-be92-af5fb4c537be")




