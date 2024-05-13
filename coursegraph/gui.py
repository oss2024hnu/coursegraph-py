import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel

#ui 파일이 실행파일과 같은 위치에 있어야함.
form_class = uic.loadUiType("Maingui.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.action_open.triggered.connect(self.openFunction)
        self.gridLayout_3.addWidget(self.label, 0, 0)
    
    def openFunction(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp *.gif)")
        if filename:  # 파일이 선택되었는지 확인
            pixmap = QPixmap(filename)  # 파일을 QPixmap 객체로 로드
            if not pixmap.isNull():  # 유효한 이미지 파일인지 확인
                self.label.setPixmap(pixmap)  # QLabel에 이미지 표시
                self.label.adjustSize()  # QLabel 크기 조정
            else:
                QMessageBox.warning(self, "유효하지 않은 이미지 파일입니다.")
        else:
            QMessageBox.warning(self, "파일을 선택하지 않았습니다.")

    #def saveFunction(self): #현재 미구현
    #    fname = QFileDialog.getOpenFileName(self)
    #    with open(fname[0], 'w', encoding = 'UTF8') as f:
    #        data = f.write()
    #    
    #    print(fname)

# 에러 발생시 정상 종료하도록 정의
def exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    sys.exit(1)

sys.excepthook = exception_hook
app = QApplication(sys.argv) 
myWindow = WindowClass() 
myWindow.show()
app.exec_()
