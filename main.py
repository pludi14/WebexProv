from flask import Flask, request, render_template
from controller import Controller



app = Flask(__name__, template_folder="./gui/htmlcss/")

controller=None

@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "GET":
        return render_template("index.html")


@app.route('/auth', methods=["POST", "GET"])
def auth():
    if request.method == "GET":
        return render_template("auth.html")


apikey="MTBmM2JhNzEtZGExMy00M2VlLWE5OTMtMGY1NmUxNWMxYTBjYjExMmMyZGQtMmMw_PF84_7d2b833a-567c-442f-be92-af5fb4c537be"


#try:
    #api.updateUser(personid="Y2lzY29zcGFyazovL3VzL1BFT1BMRS9iOGUwMWNjOS04OWM0LTQ1OTAtOWUxMS03NTU4NmVlNWQ5YmE", displayName="Bastian Schweinsteiger", licenses=["Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvN2QyYjgzM2EtNTY3Yy00NDJmLWJlOTItYWY1ZmI0YzUzN2JlOkVFXzQ5OGM3Zjg1LWZhMzUtNDM1ZC05OWVjLWE2ZWEyYTE5OGY3ZV9tYXJjZWxwbHVkcmEtZ2FzYW5kYm94LndlYmV4LmNvbQ"])
    #api.insertUser(emails=["testuser@solution-mp.de"], displayName="test User")
    #api.deleteUser(personID="Y2lzY29zcGFyazovL3VzL1BFT1BMRS9iOGUwMWNjOS04OWM0LTQ1OTAtOWUxMS03NTU4NmVlNWQ5YmE")
    #api.listUser()

#except WebexAPIException as e:
#    print("Fehler: "+e.kwargs["text"])


if __name__=="__main__":
    #app.run()
    controller = Controller()
    controller.leseExcel("/Users/mpludra/OneDrive/03_Techniker Schule/Techniker Arbeit/Kunden-Excel/Kunden-Excel-DRAFT.xlsx")
    controller.setToken("ZjgzMjYxZjItN2IwNy00N2Q2LTliYWEtOGJlMDZjNjZjODUwZDhiZjhkZmUtMjdm_PF84_7d2b833a-567c-442f-be92-af5fb4c537be")











