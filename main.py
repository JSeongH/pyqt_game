from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, uic, QtGui
import sys

import unit
import map




gui = uic.loadUiType("test.ui")[0]


class Main(QMainWindow, gui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Hello, User")
        map_path = "MapData/maze.png"

        self.size = 20

        self.isUnit = False
        
        self.set = unit.Operation(self)

        self.map = map.MapData(self.label, map_path)
        self.map.mapLoading()
        

    def redraw(self, rect):
        gap = rect.width() * 0.2
        rect.adjust(-gap, -gap, gap, gap)
        self.update(rect.toAlignedRect())
        
        
    def draw(self):
        pixmap = QPixmap(self.label.size())  # QLabel 크기에 맞는 QPixmap 생성
        pixmap.fill(Qt.transparent)  # 투명 배경
        painter = QPainter(pixmap)

        if self.isUnit == False:
            coord = QPointF(self.x, self.y)
            sizes = QSizeF(self.size, self.size)
            self.user = unit.User(QRectF(coord, sizes), QColor(0, 255, 0))
            self.isUnit = True

        brush = QBrush(self.user.color)
        painter.setBrush(brush)
        painter.drawRect(self.user.rect)

        painter.end()
        self.label.setPixmap(pixmap)  # QPixmap을 QLabel에 설정
        
        
    def keyPressEvent(self, e):
        if self.set.isStart:
            self.set.keyPressed(e.key())
        else:
            pass
            # 키를 눌렀을 때가아니라 내가 원할때 시작할 수 있는 다른 무언가가 필요
            # self.set.gameStart()
            # self.update()
            
    
    def keyReleaseEvent(self, e):
        if self.set.isStart:
            self.set.keyReleased(e.key())


    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton and self.set.isStart == False:
            local_pos = self.mapFromGlobal(e.globalPos())  
            self.x = local_pos.x()  
            self.y = local_pos.y()

            self.draw()
        
    
    def closeEvent(self, e):
        self.set.gameEnd()
        
        
    def gameOver(self):
        reply = QMessageBox.question(self, 'Game Over', '게임이 끝났습니다. 다시 시작하시겠습니까?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.set.gameStart()  # 다시 시작
        else:
            self.close()  # 게임 종료




if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = Main()
    game.show()
    sys.exit(app.exec())
    