import pathlib
from flask import Flask, request, render_template


class GUI():

    def __init__(self):
        self.__workdir = pathlib.Path().absolute()
        self.__htmlcssPath = str(self.__workdir)+"/gui/htmlcss/"


    __app = Flask(__name__, template_folder="./htmlcss/")


    @__app.route('/', methods=["POST", "GET"])
    def index():
        if request.method == "GET":
            return render_template("index.html")

    def startWebserver(self):
        self.__app.run(host="0.0.0.0", port=5000, debug=False)


