from webexapipkg.webexapi import Webexapi
from webexapipkg.webexAPIException import WebexAPIException

apikey="ZmVhN2NhODItMmRkYi00OWQ1LThlMjAtNmQxMWE5N2Y3ZDBjN2MwNDc1NGItMmVm_PF84_7d2b833a-567c-442f-be92-af5fb4c537be"
api=Webexapi(apikey=apikey)

#json = api.parseJSON("PUT_people.json")
#print(json)

try:
    api.updateUser(personid="Y2lzY29zcGFyazovL3VzL1BFT1BMRS9iOGUwMWNjOS04OWM0LTQ1OTAtOWUxMS03NTU4NmVlNWQ5YmE", displayName="Bastian Schweinsteiger", licenses=["Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvN2QyYjgzM2EtNTY3Yy00NDJmLWJlOTItYWY1ZmI0YzUzN2JlOkVFXzQ5OGM3Zjg1LWZhMzUtNDM1ZC05OWVjLWE2ZWEyYTE5OGY3ZV9tYXJjZWxwbHVkcmEtZ2FzYW5kYm94LndlYmV4LmNvbQ"])
except WebexAPIException as e:
    print("Fehler: "+e.kwargs["text"])

