import pathlib
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename


class GUI():


    def __init__(self):
        self.__workdir = pathlib.Path().absolute()
        self.__htmlcssPath = str(self.__workdir)+"/gui/htmlcss/"


    __app = Flask(__name__, template_folder="./htmlcss/")

    def checkFile(self, filename):
        #pruefe File Extension
        if not "." in filename: return False
        extension = filename.rsplit(".",1)[1] #rechts Split nur beim ersten Punkt splitten
        if extension.upper()=="XSLX":
            return True
        else: return False





    @__app.route('/', methods=["POST", "GET"])
    def index():
        if request.method == "GET":
            return render_template("readExcel.html")
        if request.method == "POST":
            excel = request.files["excelFile"]
            excel.save("FileUpload")
            return render_template("readExcel.html")

    @__app.route('/upload', methods=["POST"])
    def excelupload():
        if request.method == "POST":
            if request.files:
                excel = request.files["excelFile"]
                excelfilename=secure_filename(excel.filename) #Sichere Dateinamen (z.B. keine Leerzeichen etc.)




    def startWebserver(self):
        self.__app.run(host="0.0.0.0", port=5000, debug=False)


