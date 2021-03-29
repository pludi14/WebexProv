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

#liest den Token aus der Datei auth/token aus.
with open(authordner+"/token") as file:
    token = file.readline()
    try:
        controller.setToken(token)
        accessToken=token
        file.close()
    except WebexAPIException as e:
        accessToken="Access Token konnte nicht gesetzt werden."

#Org wird schon ausgewählt wenn die Varible oben befüllt ist.
if org:
    try:
        controller.aktuelle_Org=org
    except WebexAPIException as e:
        logger.info("Fehler: %s", e.kwargs["text"])


#Flask Route: Einstiegsseite index.html
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

#Flask Route: Excel auswählen und Prozessoption auswählen. tokenset.html
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

#Flask Route: Excel Datei wird hier per POST angenommen und eingelesen.
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

#Flask Route: Hier wird die Prozessoption angenommen und die Import Seite angezeigt.
@app.route('/starteimport', methods=["POST","GET"])
def starte_Import():
    controller.reset_Progress()

    global prozessoption
    if request.form:
        prozessoption = request.form["prozessoptionen"]

    return render_template("import.html")

#Flask Route: Prozess wird hier gestartet.
@app.route('/starteprozess', methods=["POST"])
def starte_Prozess():
    global prozessoption
    import_status="None"
    res = {}
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
        logger.info("Fehler beim Prozess.")
        res["status"] = "Fehler beim Prozess. Bitte überprüfen Sie die Log Datei."
        resjson = json.dumps(res)
        return Response(status=200, response=resjson, mimetype="text/html")

    res["status"]=import_status
    logger.info(import_status)
    resjson=json.dumps(res)
    return Response(status=200, response=resjson, mimetype='application/json')


#Flask Route: Tokenreset.
@app.route('/reset', methods=["GET"])
def tokenreset():
    controller.orgReset()
    return redirect("/")


#Flask Route: OAuth2.0 authentifizierung
@app.route('/auth', methods=["POST", "GET"])
def auth():
    global accessToken
    if request.method == "GET":
        if "code" in request.args and request.args.get("state") == "WebexProv_State":
            state = request.args.get("state")  # Captures value of the state.
            code = request.args.get("code")  # Captures value of the code.
            token=controller.oauth(code)
            accessToken = token
            return redirect("/")
        else:
            return render_template("auth.html")

#Flask Route: Hier wird der aktuelle Importprozesstatus übergeben
@app.route('/progress')
def progress():
    def generate():
        x=0
        while x <= 100:
            yield "data:" + str(x) + "\n\n"
            x=controller.get_Progress()
            time.sleep(0.5)
    return Response(generate(), mimetype='text/event-stream')


#leert den Tempordner wo die Excel Dateien temporär abgespeichert werden
def tempordner_leeren():
    shutil.rmtree(tempordner)
    os.mkdir(tempordner)
    logger.info("Tempordner geleert.")

#Wird beim Starten des Programms ausgeführt.
def main():
    tempordner_leeren()
    logging.getLogger("werkzeug").setLevel(logging.CRITICAL)
    app.run(debug=False)


if __name__=="__main__":
    main()













