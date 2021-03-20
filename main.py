from flask import Flask, request, render_template, redirect, Response
from controller import Controller
from webexapipkg.webexAPIException import WebexAPIException
from werkzeug.utils import secure_filename
import os
import shutil
import time
import logging
from log.setup_logger import logger
import json

logger = logging.getLogger("WP.main")
logger.info("________Webex Prov gestartet__________")


app = Flask(__name__, template_folder="./gui/html/")

authordner=os.path.join(os.getcwd(), "Auth")
tempordner=os.path.join(os.getcwd(), "tmp")
prozessoption=""
controller = Controller()
org=""
excel=""
accessToken=""

with open(authordner+"/token") as file:
    token = file.readline()
    print(token)
    try:
        controller.setToken(token)
        accessToken=token
        file.close()
    except WebexAPIException as e:
        accessToken=e.kwargs["text"]
        logger.info("Fehler: %s", e.kwargs["text"])

if org:
    try:
        controller.aktuelle_Org=org
    except WebexAPIException as e:
        logger.info("Fehler: %s", e.kwargs["text"])

if excel:
    try:
        controller.leseExcel(excel)
    except WebexAPIException as e:
        logger.info("Fehler: %s", e.kwargs["text"])


@app.route('/', methods=["GET","POST"])
def index():
    if request.method=="POST":
        form_data = request.form
        global accessToken
        accessToken = form_data["accessToken"]
        try:
            controller.setToken(accessToken)
        except WebexAPIException as e:
            logger.info("Fehler: %s", e.kwargs["text"])
            accessToken=e.kwargs["text"]
        return render_template("index.html", status=controller.org_Initialisiert, token=accessToken, orgs=controller.orgs)
    if request.method == "GET":
        return render_template("index.html", status=controller.org_Initialisiert, token=accessToken, orgs=controller.orgs)


@app.route('/import', methods=["GET","POST"])
def excelImport():
    if request.method=="GET":
        return render_template("tokenset.html", token=accessToken, selectedOrg=controller.aktuelle_Org)

    if request.method=="POST":
        form_data = request.form
        try:
            controller.aktuelle_Org=form_data["selectedOrg"]
            if request.files:
                excel = request.files["excelFile"]
                excelfilename = secure_filename(excel.filename)  # Sichere Dateinamen (z.B. keine Leerzeichen etc.)
        except WebexAPIException:
            logger.info("/import %s", str(WebexAPIException.kwargs))
        return render_template("tokenset.html", token=accessToken, selectedOrg=controller.aktuelle_Org)

@app.route('/readexcel', methods=["POST"])
def read_excel():
    if request.files:
        excel = request.files["excelFile"]
        excelfilename = secure_filename(excel.filename)  # Sichere Dateinamen (z.B. keine Leerzeichen etc.)
        global gui_exceldatei
        gui_exceldatei=excelfilename
        tempordner_leeren()
        try:
            excel.save(os.path.join(tempordner, excelfilename))
            controller.leseExcel(os.path.join(tempordner, excelfilename))
        except Exception:
            logger.info("Excel Datei konnte nicht eingelesen werden.")
            gui_exceldatei="Fehler: Excel konnte nicht eingelesen werden."
        return render_template("tokenset.html", token=accessToken, selectedOrg=controller.aktuelle_Org, exceldatei=gui_exceldatei)

@app.route('/starteimport', methods=["POST","GET"])
def starte_Import():
    controller.reset_Progress()
    global prozessoption
    if request.form:
        prozessoption = request.form["prozessoptionen"]

    return render_template("import.html")


@app.route('/starteprozess', methods=["POST"])
def starte_Prozess():
    global prozessoption
    import_status="None"
    try:
        if prozessoption == "1":
            controller.starte_Prozess(update=True, insert=False)
            import_status = "Update erfolgreich."
        elif prozessoption == "2":
            controller.starte_Prozess(update=False, insert=True)
            import_status = "Insert erfolgreich."
        elif prozessoption == "3":
            controller.starte_Prozess(update=True, insert=True)
            import_status = "Update + Insert erfolgreich."
        elif prozessoption == "4":
            controller.starte_Prozess(update=False, insert=False, delete=True)
            import_status = "Delete erfolgreich."

    except WebexAPIException as e:
        logger.info("Fehler: %s", e.kwargs["text"])
        return Response(status=200, response="Fehler: "+e.kwargs["text"], mimetype="text/html")
    res={}
    res["status"]=import_status
    resjson=json.dumps(res)
    return Response(status=200, response=resjson, mimetype='application/json')



@app.route('/reset', methods=["GET"])
def tokenreset():
    controller.orgReset()
    return redirect("/")



@app.route('/auth', methods=["POST", "GET"])
def auth():
    if request.method == "GET":
        if "code" in request.args and request.args.get("state") == "WebexProv_State":
            state = request.args.get("state")  # Captures value of the state.
            code = request.args.get("code")  # Captures value of the code.
            controller.oauth(code)
            return redirect("/")
        else:
            return render_template("auth.html")


@app.route('/progress')
def progress():
    def generate():
        x=0
        while x <= 100:
            yield "data:" + str(x) + "\n\n"
            x=controller.get_Progress()
            time.sleep(0.5)
    return Response(generate(), mimetype='text/event-stream')




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
    logger.info("Tempordner geleert.")

def main():
    tempordner_leeren()
    app.run(debug=True)

if __name__=="__main__":
    main()













