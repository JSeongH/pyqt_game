from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import  *
from PyQt5 import uic
from threading import Thread
import time
import sys
import cv2



 

gui = uic.loadUiType("test.ui")[0]


class Unit():
    def __init__(self, rect=QRectF(), color=QColor()):
        self.rect = rect
        self.color = color

        self.direction = [False, False, False, False]

    
    def keyUpdate(self, key, isPress=True):
        if key == Qt.Key_Left:
            self.direction[0] = isPress
        if key == Qt.Key_Up:
            self.direction[1] = isPress
        if key == Qt.Key_Right:
            self.direction[2] = isPress
        if key == Qt.Key_Down:
            self.direction[3] = isPress


    def moveUpdate(self, speed=2.0):
        if self.direction[0]:  # 왼쪽
            self.rect.adjust(-speed, 0, -speed, 0)
        if self.direction[1]:  # 위
            self.rect.adjust(0, -speed, 0, -speed)
        if self.direction[2]:  # 오른쪽
            self.rect.adjust(speed, 0, speed, 0)
        if self.direction[3]:  # 아래
            self.rect.adjust(0, speed, 0, speed)



class MyWindow(QMainWindow, gui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.isStart = False
        self.isCollid = False
        self.unit = None

        self.boundary = self.label.rect()
        self.target_color = QColor(255, 255, 255)

        self.path = "MapData\maze.png"
        self.image = cv2.imread(self.path, cv2.IMREAD_GRAYSCALE)
        _, self.threshold_image = cv2.threshold(self.image, 127, 255, cv2.THRESH_BINARY_INV)
        
        pixmap = QPixmap(self.label.size())
        pixmap.fill(Qt.transparent)
        self.label.setPixmap(pixmap)
        self.target_pixmap = self.label.pixmap()


    def gameStart(self):
        if self.unit:
            self.isStart = True

            self.thread = Thread(target=self.threadFunc)
            self.thread.start()
        else:
            QMessageBox.information(self, '시작에러', '화면을 클릭해 유닛을 생성해주세요.', QMessageBox.Yes)

    
    def gameStop(self):
        self.isStart = False

    
    def drawRectAtCoordinates(self, x, y):
        if self.isStart == False:
            coord = QPoint(x, y)
            sizes = QSizeF(20, 20)
            self.unit = Unit(QRectF(coord, sizes), QColor(0, 255, 0))
            self.update()


    def draw(self, painter):
        if self.unit:
            brush = QBrush(self.unit.color)
            painter.setBrush(brush)
            painter.drawRect(self.unit.rect)

    
    def paintEvent(self, e):
        painter = QPainter(self.target_pixmap)
        maze_pixmap = QPixmap(self.path)
        scaled_pixmap = maze_pixmap.scaled(800, 800, Qt.IgnoreAspectRatio)
        painter.drawPixmap(0, 0, scaled_pixmap)
        self.draw(painter)
            

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton and self.isStart == False:
            local_pos = self.mapFromGlobal(e.globalPos())  
            x = local_pos.x()
            y = local_pos.y()

            self.drawRectAtCoordinates(x, y)


    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.gameStop()
            self.close()
        if e.key() == Qt.Key_Space:
            self.gameStart()
        if e.key() == Qt.Key_Q:
            self.gameStop()
        else:
            self.unit.keyUpdate(e.key(), True)
            self.update()

    
    def keyReleaseEvent(self, e):
        self.unit.keyUpdate(e.key(), False)
            

    def threadFunc(self):
        while self.isStart:
            self.unit.moveUpdate()
            self.update()

            time.sleep(0.01)

 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())