from flask import Flask, request, render_template
from controller import Controller



app = Flask(__name__, template_folder="./gui/htmlcss/")

controller = Controller()
accessToken=None

@app.route('/', methods=["GET","POST"])
def index():
    if request.method=="POST":
        form_data = request.form
        global accessToken
        accessToken = form_data["accessToken"]
        controller.setToken(accessToken)
        return render_template("index.html", status=controller.org_Initialisiert, token=accessToken, orgs=controller.orgs)
    if request.method == "GET":
        return render_template("index.html", status=controller.org_Initialisiert, token=accessToken, orgs=controller.orgs)


@app.route('/excelimport', methods=["GET","POST"])
def excelImport():
    if request.method=="GET":
        return render_template("tokenset.html", token=accessToken, selectedOrg=controller.aktuelle_Org)

    if request.method=="POST":
        form_data = request.form
        #print(form_data["selectedOrg"])
        controller.aktuelle_Org=form_data["selectedOrg"]
        return render_template("tokenset.html", token=accessToken, selectedOrg=controller.aktuelle_Org)


@app.route('/auth', methods=["POST", "GET"])
def auth():
    if request.method == "GET":
        return render_template("auth.html")


apitoken="NThlMzRmMjUtZmU1Zi00OGJiLTg3MjEtMTg4MGJkMTE1NTI5Y2I5MzBjYTQtNTk5_PE93_f0cd0058-e08e-47f9-a0d5-5940d6ccb6ab"


#try:
    #api.updateUser(personid="Y2lzY29zcGFyazovL3VzL1BFT1BMRS9iOGUwMWNjOS04OWM0LTQ1OTAtOWUxMS03NTU4NmVlNWQ5YmE", displayName="Bastian Schweinsteiger", licenses=["Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvN2QyYjgzM2EtNTY3Yy00NDJmLWJlOTItYWY1ZmI0YzUzN2JlOkVFXzQ5OGM3Zjg1LWZhMzUtNDM1ZC05OWVjLWE2ZWEyYTE5OGY3ZV9tYXJjZWxwbHVkcmEtZ2FzYW5kYm94LndlYmV4LmNvbQ"])
    #api.insertUser(emails=["testuser@solution-mp.de"], displayName="test User")
    #api.deleteUser(personID="Y2lzY29zcGFyazovL3VzL1BFT1BMRS9iOGUwMWNjOS04OWM0LTQ1OTAtOWUxMS03NTU4NmVlNWQ5YmE")
    #api.listUser()

#except WebexAPIException as e:
#    print("Fehler: "+e.kwargs["text"])


if __name__=="__main__":
    app.run(debug=True)

    #controller.setToken(apitoken)
    #controller.aktuelle_Org="Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi9mMGNkMDA1OC1lMDhlLTQ3ZjktYTBkNS01OTQwZDZjY2I2YWI"
    #controller.leseExcel("/Users/mpludra/OneDrive/03_Techniker Schule/Techniker Arbeit/Kunden-Excel/Kunden-Excel-DRAFT.xlsx")
    #controller.starte_Prozess(update=True,insert=False)











