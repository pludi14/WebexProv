import requests
from webexapipkg.webexAPIException import WebexAPIException
import json
import os
import pathlib
import logging
from http.client import HTTPConnection


class Webexapi():

    def __init__(self, apikey=""):
        self.__apikey = apikey
        self.__path = pathlib.Path(__file__).parent.absolute()
        self.__workdir = pathlib.Path().absolute()
        self.__referencePath = str(self.__workdir)+"/webexapipkg/reference/"

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
        httpHeaders = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.__apikey}

        #print(apiUrl)

        if methode=="GET":
            response = requests.get(url=apiUrl, headers=httpHeaders, params=queryParameter)
            responsetext = json.loads(response.text)
        if methode=="PUT":
            response = requests.put(url=apiUrl, headers=httpHeaders, params=queryParameter, data=querryData)
            responsetext = json.loads(response.text)
        if methode=="POST":
            response = requests.post(url=apiUrl, headers=httpHeaders, params=queryParameter, data=querryData)
            responsetext = json.loads(response.text)
        if methode=="DELETE":
            response = requests.delete(url=apiUrl, headers=httpHeaders, params=queryParameter)
            responsetext = json.loads(response.text)

        if response.status_code == 200:
            return responsetext
        else:
            raise WebexAPIException(statuscode=response.status_code, text=responsetext["message"]);


    def __setApikey(self, apikey=""):
        self.__apikey=apikey

    def listUser(self, **kwargs):
        queryParams = kwargs if kwargs else {}

        #if kwargs:
        #    for key in kwargs:
        #        queryParams[key] = kwargs[key]

        response=self.__createRequest("people", "GET", queryParams)
        print(response)
        return response


    def insertUser(self, **kwargs):

        data = {}

        for key in kwargs:
            data[key] = kwargs[key]

        queryParams = {"callingData:" "true"}
        jsondata = json.dumps(data)

        response = self.__createRequest("people", "POST", querryData=jsondata)

        print(response)
        return response


    def deleteUser(self, personID=""):

        response = self.__createRequest("people/"+personID, "DELETE")
        print(response)
        return response


    def updateUser(self, **kwargs):

        personID = kwargs.pop("personid")
        data = {}

        for key in kwargs:
            data[key]=kwargs[key]


        queryParams = {"callingData:" "true"}
        jsondata=json.dumps(data)

        response = self.__createRequest("people/"+personID, "PUT", querryData=jsondata)
        print(response)
        return response


    def parseJSON(self, datei):
        #wird gar nicht genutzt

        with open(os.path.join(self.__referencePath,datei)) as file:
            parsedJSON = json.load(file)
            return parsedJSON


if __name__=="__main__":
    api=Webexapi(apikey="ZmVhN2NhODItMmRkYi00OWQ1LThlMjAtNmQxMWE5N2Y3ZDBjN2MwNDc1NGItMmVm_PF84_7d2b833a-567c-442f-be92-af5fb4c537be")




