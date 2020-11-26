import requests
from webexapipkg.webexAPIException import WebexAPIException
import json

class Webexapi():

    def __init__(self, apikey=""):
        self.__apikey = apikey


    def __createRequest(self, urlZiel, methode, queryParameter):
        apiUrl = "https://webexapis.com/v1/"+urlZiel
        httpHeaders = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.__apikey}

        if methode=="GET":
            response = requests.get(url=apiUrl, headers=httpHeaders, params=queryParameter)

        return response


    def __setApikey(self, apikey=""):
        self.__apikey=apikey

    def listUser(self):
        queryParams = {}
        response=self.__createRequest("people", "GET", queryParams)
        responsetext = json.loads(response.text)
        if response.status_code==200:
            return responsetext
        else:
            raise WebexAPIException(statuscode=response.status_code, text=responsetext["message"]);



    def insertUser(self):
        print("Muss noch implementiert werden.")



if __name__=="__main__":
    api=Webexapi(apikey="MTVhM2NlOGUtMTA1Mi00YWI0LTk2ZTMtNjE3YjM2NjVjY2VlYjRmNmIxNDItYjU1_PF84_7d2b833a-567c-442f-be92-af5fb4c537be")
    try:
        users=api.listUser()
        print((users["items"]))

    except WebexAPIException as e:
        print("Fehler: "+e.kwargs["text"])

