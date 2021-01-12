from openpyxl import load_workbook
import pathlib

class Excelhandler():

    def __init__(self):
        self.__dateiname = ""
        self.__path = pathlib.Path(__file__).parent.absolute()
        self.__workdir = pathlib.Path().absolute()

    def __setDateiname(self,x): self.__dateiname =x
    def __getDateiname(self): return self.__dateiname
    dateiname=property(__getDateiname,__setDateiname)  # Get und set kan dann über den Variablennamen direkt ausgeführt werden.
                                                       # Nur für den Verwender der Klasse nicht innerhalb der Klasse  Verwenden

    def leseExcel(self, datei=""):
        exceldatei= self.__dateiname if self.__dateiname else datei
        print(exceldatei)
        wb = load_workbook(filename=exceldatei)
        daten=wb["Daten"]




if __name__=="__main__":
    handler = Excelhandler()
    handler.dateiname="Kunden-Excel-DRAFT.xlsx"

    handler.leseExcel()


