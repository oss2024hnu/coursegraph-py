import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

#ui 파일이 실행파일과 같은 위치에 있어야함.
form_class = uic.loadUiType("Maingui.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

# 에러 발생시 정상 종료하도록 정의
def exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    sys.exit(1)

sys.excepthook = exception_hook
app = QApplication(sys.argv) 
myWindow = WindowClass() 
myWindow.show()
app.exec_()
