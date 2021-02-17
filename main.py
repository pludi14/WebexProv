from flask import Flask, request, render_template, redirect
from controller import Controller
from webexapipkg.webexAPIException import WebexAPIException
from werkzeug.utils import secure_filename
import os
import shutil


app = Flask(__name__, template_folder="./gui/htmlcss/")

tempordner=os.path.join(os.getcwd(), "tmp")


controller = Controller()
accessToken="MDQxNzhmMWMtOTQzNS00MjY2LTg2ZmItZmE4NDRjZGVhYjZkZWYzOGY0ZjYtZWY0_PE93_f0cd0058-e08e-47f9-a0d5-5940d6ccb6ab"

if accessToken:
    controller.setToken(accessToken)

@app.route('/', methods=["GET","POST"])
def index():
    if request.method=="POST":
        form_data = request.form
        global accessToken
        accessToken = form_data["accessToken"]
        try:
            controller.setToken(accessToken)
        except WebexAPIException as e:
            print("Fehler: "+e.kwargs["text"])

        return render_template("index.html", status=controller.org_Initialisiert, token=accessToken, orgs=controller.orgs)
    if request.method == "GET":
        return render_template("index.html", status=controller.org_Initialisiert, token=accessToken, orgs=controller.orgs)


@app.route('/import', methods=["GET","POST"])
def excelImport():
    if request.method=="GET":
        return render_template("tokenset.html", token=accessToken, selectedOrg=controller.aktuelle_Org)
    if request.method=="POST":
        form_data = request.form
        controller.aktuelle_Org=form_data["selectedOrg"]
        if request.files:
            excel = request.files["excelFile"]
            excelfilename = secure_filename(excel.filename)  # Sichere Dateinamen (z.B. keine Leerzeichen etc.)
        return render_template("tokenset.html", token=accessToken, selectedOrg=controller.aktuelle_Org)

@app.route('/readexcel', methods=["POST"])
def read_excel():
    if request.files:
        excel = request.files["excelFile"]
        excelfilename = secure_filename(excel.filename)  # Sichere Dateinamen (z.B. keine Leerzeichen etc.)
        global gui_exceldatei
        gui_exceldatei=excelfilename
        tempordner_leeren()
        excel.save(tempordner+excelfilename)
        try:
            controller.leseExcel(tempordner+excelfilename)
        except:
            print("Excel konnte nicht eingelesen werden.")
            gui_exceldatei=None
        return render_template("tokenset.html", token=accessToken, selectedOrg=controller.aktuelle_Org, exceldatei=gui_exceldatei)

@app.route('/starteimport', methods=["POST"])
def starte_Import():
    form_data = request.form

    if form_data["prozessoptionen"]=="1":
        #return render_template("import.html")
        controller.starte_Prozess(update=True,insert=False)


    elif form_data["prozessoptionen"]=="2":
        #return render_template("import.html")
        controller.starte_Prozess(update=False, insert=True)


    elif form_data["prozessoptionen"]=="3":
        #return render_template("import.html")
        controller.starte_Prozess(update=True, insert=True)

    return render_template("import.html")



@app.route('/reset', methods=["GET"])
def tokenreset():
    controller.orgReset()
    return redirect("/")



@app.route('/auth', methods=["POST", "GET"])
def auth():
    if request.method == "GET":
        return render_template("auth.html")





#try:
    #api.updateUser(personid="Y2lzY29zcGFyazovL3VzL1BFT1BMRS9iOGUwMWNjOS04OWM0LTQ1OTAtOWUxMS03NTU4NmVlNWQ5YmE", displayName="Bastian Schweinsteiger", licenses=["Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvN2QyYjgzM2EtNTY3Yy00NDJmLWJlOTItYWY1ZmI0YzUzN2JlOkVFXzQ5OGM3Zjg1LWZhMzUtNDM1ZC05OWVjLWE2ZWEyYTE5OGY3ZV9tYXJjZWxwbHVkcmEtZ2FzYW5kYm94LndlYmV4LmNvbQ"])
    #api.insertUser(emails=["testuser@solution-mp.de"], displayName="test User")
    #api.deleteUser(personID="Y2lzY29zcGFyazovL3VzL1BFT1BMRS9iOGUwMWNjOS04OWM0LTQ1OTAtOWUxMS03NTU4NmVlNWQ5YmE")
    #api.listUser()

#except WebexAPIException as e:
#    print("Fehler: "+e.kwargs["text"])

def tempordner_leeren():
    shutil.rmtree(tempordner)
    os.mkdir(tempordner)



if __name__=="__main__":
    tempordner_leeren()
    app.run(debug=True)


    #controller.setToken(apitoken)
    #controller.aktuelle_Org="Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi9mMGNkMDA1OC1lMDhlLTQ3ZjktYTBkNS01OTQwZDZjY2I2YWI"
    #controller.leseExcel("/Users/mpludra/OneDrive/03_Techniker Schule/Techniker Arbeit/WebexProv/Kunden-Excel/Kunden-Excel-DRAFT.xlsx")
    #controller.delete_User_Prozess()
    #controller.starte_Prozess(update=True,insert=True)











