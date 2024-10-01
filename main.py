from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, uic, QtGui
from threading import Thread
import sys
import time

import unit
import map

## start 버튼 혹은 키입력 받아서 움직여보기 
## 움직이는게 통과되면 상호작용이 가능하게 맵을 그려보기
## 이후 충돌여부에 따라 게임 상태 변화
## 조이스틱으로 움직이는 기능 추가 



gui = uic.loadUiType("test.ui")[0]


class Main(QMainWindow, gui):
    update_widget = pyqtSignal(QRectF)
    game_over = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Hello, User")
        map_path = "MapData/maze.png"
        self.isStart = False

        self.size = 20

        self.isUnit = False
        
        self.set = unit.Operation(self)

        # self.map = map.MapData(self.label, map_path)
        # self.map.mapLoading()

        self.update_widget.connect(self.redraw)
        self.game_over.connect(self.gameOver)

        
    def draw(self):
        pixmap = QPixmap(self.label.size())  # QLabel 크기에 맞는 QPixmap 생성
        pixmap.fill(Qt.transparent)  # 투명 배경
        painter = QPainter(pixmap)

        if self.set.isStart == False:
            coord = QPointF(self.x, self.y)
            sizes = QSizeF(self.size, self.size)
            self.user = unit.User(QRectF(coord, sizes), QColor(0, 255, 0))
            self.isUnit = True
            self.gameStart()


        brush = QBrush(self.user.color)
        painter.setBrush(brush)
        painter.drawRect(self.user.rect)

        painter.end()
        self.label.setPixmap(pixmap)  # QPixmap을 QLabel에 설정


    def redraw(self, rect):
        gap = rect.width() * 0.2
        rect.adjust(-gap, -gap, gap, gap)

        self.draw()


    def gameStart(self):
        self.isStart = True

        self.t = Thread(target=self.theard)
        self.t.start()

        
    def gameEnd(self):
        self.isStart = False

    
    def gameOver(self):
        reply = QMessageBox.question(self, 'Game Over', '게임이 끝났습니다. 다시 시작하시겠습니까?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.gameStart()  # 다시 시작
        else:
            self.close()  # 게임 종료
        
        
    def keyPressEvent(self, e):
        if self.isStart:
            self.user.keyUpdate(e.key(), True)
        else:
            self.user.keyUpdate(e.key(), True)
            # 키를 눌렀을 때가아니라 내가 원할때 시작할 수 있는 다른 무언가가 필요
            # self.set.gameStart()
            # self.update()
            
    
    def keyReleaseEvent(self, e):
        if self.isStart:
            self.user.keyUpdate(e.key(), False)


    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton and self.set.isStart == False:
            local_pos = self.mapFromGlobal(e.globalPos())  
            self.x = local_pos.x()  
            self.y = local_pos.y()

            self.draw()
        
    
    def closeEvent(self, e):
        self.gameEnd()
        
    
    def update(self):
        self.update_widget.emit(self.user.rect)


    def theard(self):
        while self.isStart:
            self.user.moveUpdate()
            self.update()
            
            if self.user.isCollided:
                self.game_over.emit()
                break
            
            time.sleep(0.01)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = Main()
    game.show()
    sys.exit(app.exec())
    