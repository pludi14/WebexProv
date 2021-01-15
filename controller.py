from excelpkg.excel import Excelhandler
from webexapipkg.webexapi import Webexapi


class Controller():
    def __init__(self):
        self.__api=Webexapi()
        self.__excelhandler=Excelhandler()


    def leseExcel(self,exceldatei):
        self.__excelhandler.leseExcel(exceldatei)






