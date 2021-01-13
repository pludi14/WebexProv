from openpyxl import load_workbook
import pathlib

class Excelhandler():

    def __init__(self, datei=""):
        self.__dateiname = datei
        self.__path = pathlib.Path(__file__).parent.absolute()
        self.__workdir = pathlib.Path().absolute()
        self.__daten_sheet=""
        self.__anzahlDatensaetze=0
        self.__alleRows=None

    def __setDateiname(self,x): self.__dateiname =x
    def __getDateiname(self): return self.__dateiname
    dateiname=property(__getDateiname,__setDateiname)  # Get und set kan dann über den Variablennamen direkt ausgeführt werden.
                                                       # Nur für den Verwender der Klasse nicht innerhalb der Klasse  Verwenden

    def leseExcel(self, datei=""):
        exceldatei= self.__dateiname if self.__dateiname else datei
        wb = load_workbook(filename=exceldatei)
        self.__daten_sheet=wb["Daten"]
        self.__anzahlDatensaetze=self.__getAnzahlDatensaetze()
        self.__alleRows=self.__daten_sheet.rows




    def __getAnzahlDatensaetze(self):
        wertvorhanden=True
        zaehler=0
        row=2
        while wertvorhanden:
            zellenwert = self.__daten_sheet["C"+str(row)].value
            if zellenwert == None:
                wertvorhanden=False
            else:
                zaehler=zaehler+1
                row=row+1
        print(zaehler)
        return zaehler

    def getDaten(self):
        daten=[]

        for zeile in self.__alleRows:
            datensatz={}
            datensatz["firstName"]=zeile[0].value
            datensatz["lastName"] = zeile[0].value
            datensatz["emails"]=zeile[2].value


            daten.append(datensatz)

        print(daten)







if __name__=="__main__":
    handler = Excelhandler()
    handler.dateiname="Kunden-Excel-DRAFT.xlsx"

    handler.leseExcel()
    handler.getDaten()


