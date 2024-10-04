from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import  *
from PyQt5 import uic
from threading import Thread
import datetime
import time
import sys
import cv2
import numpy as np


 

gui = uic.loadUiType("test.ui")[0]



class Working(QThread):
    update_signal = pyqtSignal()
    update_unit = pyqtSignal(QRectF)
    
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.running = True
        
        
    def run(self):
        while self.running:
            self.update_unit.emit(self.parent.unit.rect)
            self.update_signal.emit()
            time.sleep(0.01)
            
            
    def resume(self):
        self.running = True
        
    
    def pause(self):
        self.running = False



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
        self.unit = None
        self.writer = None

        self.unit_color = QColor(0, 255, 0)
        self.unit_size = 20
        self.start_x = None
        self.start_y = None

        self.boundary = self.label.rect()
        self.target_color = 255
        self.pixmap_size = (800, 800)

        self.path = "MapData/maze.png"
        self.image = cv2.imread(self.path, cv2.IMREAD_GRAYSCALE)
        _, self.threshold_image = cv2.threshold(self.image, 127, 255, cv2.THRESH_BINARY_INV)
        self.threshold_image = cv2.resize(self.threshold_image, self.pixmap_size)
        
        self.work_thread = Working(self)
        self.work_thread.update_signal.connect(self.updateImage)
        self.work_thread.update_unit.connect(self.updateUnit)
        
        pixmap = QPixmap(self.label.size())
        pixmap.fill(Qt.transparent)
        self.label.setPixmap(pixmap)
        self.target_pixmap = self.label.pixmap()


    def gameStart(self):
        if self.unit:
            self.isStart = True
            if self.work_thread.running == False:
                self.work_thread.resume()
            self.work_thread.start()
            self.recordImage()
        else:
            QMessageBox.information(self, '유닛이 없습니다.', '화면을 클릭해 유닛을 생성해주세요.', QMessageBox.Yes)

    
    def gameStop(self):
        self.isStart = False
        self.work_thread.pause()
        
    
    def gameOver(self):
        self.isStart = False
        self.work_thread.pause()
        reply = QMessageBox.question(self, 'Game Over', '다시하기(Yes) | 게임종료(No)', QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.gameReset()
            self.gameStart()
        else:
            self.gameStop()
            QApplication.quit()

    
    def gameReset(self):
        self.gameSnapshot()

    
    def detectWall(self):
        left = int(self.unit.rect.left())
        right = int(self.unit.rect.right())
        top = int(self.unit.rect.top())
        bottom = int(self.unit.rect.bottom())

        if np.any(self.threshold_image[top:bottom, left:right] == self.target_color):
            self.gameOver()

    
    def drawRectAtCoordinates(self, x, y):
        if self.isStart == False:
            coord = QPoint(x, y)
            sizes = QSizeF(self.unit_size, self.unit_size)
            self.unit = Unit(QRectF(coord, sizes),self.unit_color)
            self.updateUnit()


    def draw(self, painter):
        if self.unit:
            brush = QBrush(self.unit.color)
            painter.setBrush(brush)
            painter.drawRect(self.unit.rect)

    
    def paintEvent(self, e):
        painter = QPainter(self.target_pixmap)
        maze_pixmap = QPixmap(self.path)
        scaled_pixmap = maze_pixmap.scaled(self.pixmap_size[0], self.pixmap_size[1], Qt.IgnoreAspectRatio)
        painter.drawPixmap(0, 0, scaled_pixmap)
        self.draw(painter)
            

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton and self.isStart == False:
            local_pos = self.mapFromGlobal(e.globalPos())  
            x = local_pos.x()
            y = local_pos.y()

            self.start_x = x
            self.start_y = y

            self.drawRectAtCoordinates(x, y)


    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.gameStop()
            QApplication.quit()
        if e.key() == Qt.Key_Q:
            self.gameStart()
        if e.key() == Qt.Key_W:
            self.gameStop()
        if e.key() == Qt.Key_R:
            self.gameReset()
        if e.key() == Qt.Key_C:
            self.captureImage()
        if e.key() == Qt.Key_Z:
            pass
        else:
            if self.unit:
                self.unit.keyUpdate(e.key(), True)
                self.update()

    
    def keyReleaseEvent(self, e):
        self.unit.keyUpdate(e.key(), False)


    def gameSnapshot(self):
        self.drawRectAtCoordinates(self.start_x, self.start_y)
        
    
    def updateUnit(self):
        self.unit.moveUpdate()
        self.detectWall()
        self.update()
        
        
    def updateImage(self):
        self.image = self.pixmapToArray(self.target_pixmap)
        if self.writer is not None:
            self.writer.write(self.image)
        
        
    def pixmapToArray(self, pixmap):
        """QPixmap을 numpy 배열로 변환"""
        image = pixmap.toImage()
        image = image.convertToFormat(QImage.Format.Format_RGB32)
        width = image.width()
        height = image.height()

        ptr = image.bits()
        ptr.setsize(image.byteCount())
        arr = np.array(ptr).reshape(height, width, 4)  # RGBA로 변환
        return cv2.cvtColor(arr, cv2.COLOR_RGBA2BGR)  # OpenCV 형식 BGR로 변환
        
    
    def captureImage(self):
        if self.isStart:
            now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = now + '.png'
            file_path = '../' + filename

            cv2.imwrite(file_path, self.image)
        else:
            print("먼저 시작해주세요.")
            
            
    def recordImage(self):
        if self.isStart:
            print("녹화중")
            now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = now + '.avi'
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            file_path = '../' + filename

            self.writer = cv2.VideoWriter(file_path, fourcc, 20.0, self.pixmap_size)
        else:
            print("먼저 시작해주세요.")
            
            
    def readVideo(self):
        
        
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())