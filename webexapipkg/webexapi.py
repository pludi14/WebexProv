import requests
from webexapipkg.webexAPIException import WebexAPIException
import json
import os
import pathlib
import logging
from http.client import HTTPConnection
import asyncio


class Webexapi():

    def __init__(self, apikey=""):
        self.__apiToken = apikey
        self.__path = pathlib.Path(__file__).parent.absolute()
        self.__workdir = pathlib.Path().absolute()
        self.__referencePath = str(self.__workdir)+"/webexapipkg/reference/"


    def __setApiToken(self, x): self.__apiToken =x
    def __getApiToken(self): return self.__apiToken
    apiToken=property(__getApiToken, __setApiToken)

    log = logging.getLogger('urllib3')
    log.setLevel(logging.DEBUG)

    # logging from urllib3 to console
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    log.addHandler(ch)

    # print statements from `http.client.HTTPConnection` to console/stdout
    # Auf 1 setzen für Debug
    HTTPConnection.debuglevel = 0




    def __createRequest(self, urlZiel, methode, queryParameter={}, querryData=""):
        apiUrl = "https://webexapis.com/v1/"+urlZiel
        httpHeaders = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.__apiToken}

        #print(apiUrl)

        if methode=="GET":
            response = requests.get(url=apiUrl, headers=httpHeaders, params=queryParameter)
            responsetext = json.loads(response.text)
            #print(responsetext)
        if methode=="PUT":
            response = requests.put(url=apiUrl, headers=httpHeaders, params=queryParameter, data=querryData)
            responsetext = json.loads(response.text)
        if methode=="POST":
            response = requests.post(url=apiUrl, headers=httpHeaders, params=queryParameter, data=querryData)
            responsetext = json.loads(response.text)
            print(responsetext)
        if methode=="DELETE":
            response = requests.delete(url=apiUrl, headers=httpHeaders, params=queryParameter)
            responsetext = json.loads(response.text)

        if response.status_code == 200:
            return responsetext
        else:
            raise WebexAPIException(statuscode=response.status_code, text=responsetext["message"]);


    def get_User(self, **kwargs):
        queryParams = kwargs if kwargs else {}
        response=self.__createRequest("people", "GET", queryParams)
        return response["items"]


    def insertUser(self, daten):

        data = daten

        #for key in kwargs:
        #    data[key] = kwargs[key]

        queryParams = {"callingData:" "true"}
        jsondata = json.dumps(data)

        response = self.__createRequest("people", "POST", querryData=jsondata)

        return response


    def deleteUser(self, personID=""):

        response = self.__createRequest("people/"+personID, "DELETE")
        print(response)
        return response


    def updateUser(self, personid ,daten):

        personID = personid
        #data = {}

        #for key in kwargs:
        #    data[key]=kwargs[key]

        #queryParams = {"callingData:" "true"}
        jsondata=json.dumps(daten)

        response = self.__createRequest("people/"+personID, "PUT", querryData=jsondata)
        print(response)
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



    def parseJSON(self, datei):
        #wird gar nicht genutzt

        with open(os.path.join(self.__referencePath,datei)) as file:
            parsedJSON = json.load(file)
            return parsedJSON


if __name__=="__main__":
    api=Webexapi(apikey="ZmVhN2NhODItMmRkYi00OWQ1LThlMjAtNmQxMWE5N2Y3ZDBjN2MwNDc1NGItMmVm_PF84_7d2b833a-567c-442f-be92-af5fb4c537be")




