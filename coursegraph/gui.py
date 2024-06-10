import sys
import subprocess
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QPixmap


# ui 파일이 실행 파일과 같은 위치에 있어야 함.
form_class = uic.loadUiType("Maingui.ui")[0]

# 화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.action_open.triggered.connect(self.openFunction) 
        self.action_othernamesave.triggered.connect(self.saveAsFunction) 
        self.pushButton.clicked.connect(self.clearImage)

        #사용할 명령어를 배열로 저장
        #0으로 초기화
        self.command_list = [0, 0]

        #table, graph, schema 체크박스와 연결
        self.radioButton_1.clicked.connect(self.check_radio)
        self.radioButton_2.clicked.connect(self.check_radio)
        self.radioButton_3.clicked.connect(self.check_radio)
        
        #파일 찾기 버튼을 push버튼과 연결
        self.pushButton_3.clicked.connect(self.select_file)

        #실행 버튼을 push버튼과 연결
        self.pushButton_2.clicked.connect(self.make_image)
        

    #라디오 버튼에서 어떤 종류인지 확인
    def check_radio(self):
        if self.radioButton_1.isChecked():
            print("table")
            self.command_list[0] = "table"
        elif self.radioButton_2.isChecked():
            print("graph")
            self.command_list[0] = "graph"
        elif self.radioButton_3.isChecked():
            print("schema")
            self.command_list[0] = "schema"

    def select_file(self):
        #QFileDialog.getOpenFileName함수를 사용해서 yaml파일만 가져올 수 있게 설정
        filename, _ = QFileDialog.getOpenFileName(self, "Open Yaml", "", "Yaml Files (*.yaml)")
        #data/[yaml파일]이 시작되는 부분
        index = 42
        #주소만 가져올 수 있게 문자열 슬라이싱
        new_filename = filename[index:]
        print(new_filename)
        self.command_list[1] = new_filename

    def make_image(self):
        #__main__.py에서 실행할 명령어 만들기
        input_file = os.path.join("../", self.command_list[1])
        print("사용할 파일 : " + input_file)
        #출력할 파일 이름 가져오기
        output_file = os.path.join("../out/", self.textEdit.toPlainText())
        print("출력할 파일이름 : " + output_file)
        #어떤 방법으로 출력할 건지 명령어 가져오기
        format = self.command_list[0]
        print("출력할 방법 : " + format)

        #만든 이미지 파일 저장할 디렉터리
        find_dir = '../out'
        if os.path.isdir(find_dir):
            pass
        else:
            self.move_path("out")
        #명령어 실행
        result = subprocess.run([sys.executable, "__main__.py", "-i", input_file, "-o", output_file, "-f", format])
        #output_file변수에 .png를 추가해서 주소를 찾을 수 있게 변경
        output_file = output_file + ".png"
        if result.returncode == 0:
            # 프로세스가 성공적으로 종료된 경우
            if os.path.exists(output_file):
                pixmap = QPixmap(output_file)  # 파일을 QPixmap 객체로 로드
                if not pixmap.isNull():
                    self.label.setPixmap(pixmap)
                    self.label.setScaledContents(True)  # 이미지 크기에 맞게 QLabel 크기 조정
                    self.label.adjustSize()  # QLabel 크기 조정
                else:
                    QMessageBox.warning(self, "Warning", "유효하지 않은 이미지 파일입니다.")
            else:
                QMessageBox.warning(self, "Warning", "출력 파일을 찾을 수 없습니다.")
        else:
            QMessageBox.warning(self, "Warning", "이미지 생성에 실패했습니다.")
        

    def openFunction(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp *.gif)")
        if filename:  # 파일이 선택되었는지 확인
            pixmap = QPixmap(filename)  # 파일을 QPixmap 객체로 로드
            if not pixmap.isNull():  # 유효한 이미지 파일인지 확인
                self.label.setPixmap(pixmap)
                self.label.setScaledContents(True)  # 이미지 크기에 맞게 QLabel 크기 조정
                self.label.adjustSize()  # QLabel 크기 조정
                self.adjustSize() # 윈도우 크기 조정
                self.statusBar().showMessage(f"Opened image: {filename}", 5000) # 상태바에 메시지 표시
                self.addRecentFile(filename) # 최근 파일 목록에 추가
            else:
                QMessageBox.warning(self, "유효하지 않은 이미지 파일입니다.")
        else:
            return

    def clearImage(self):
        self.label.clear()  # QLabel에 표시된 이미지 제거

    def saveAsFunction(self):
        try:
            filename, _ = QFileDialog.getSaveFileName(self, "Save Image As", "", "PNG Files (*.png);;JPEG Files (*.jpg);;BMP Files (*.bmp);;GIF Files (*.gif)")
            if filename:  # 파일이 선택되었는지 확인
                pixmap = self.label.pixmap()  # QLabel에 표시된 이미지 가져오기
                if pixmap:
                    pixmap.save(filename)  # 이미지를 지정된 파일 경로에 저장
                else:
                    QMessageBox.warning(self, "Warning", "이미지가 없습니다.", QMessageBox.Ok)
        except TypeError:
            QMessageBox.warning(self, "Warning", "파일 저장에 실패했습니다.", QMessageBox.Ok)

    def move_path(self, new_dir):
      # 현재 작업 디렉터리 저장
      original_directory = os.getcwd()

      # 현재 스크립트의 디렉터리 경로 얻기
      current_directory = os.path.dirname(os.path.abspath(__file__))
      
      # 상위 디렉터리 경로 계산
      parent_directory = os.path.dirname(current_directory)
      
      # 상위 디렉터리로 이동
      os.chdir(parent_directory)
      
      #생성한 이미지를 저장할 디렉터리 생성
      os.mkdir(new_dir)

      # 원래 디렉터리로 이동
      os.chdir(original_directory)

# 에러 발생 시 정상 종료하도록 정의
def exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    sys.exit(1)

sys.excepthook = exception_hook
app = QApplication(sys.argv)
myWindow = WindowClass()
myWindow.show()
app.exec_()
