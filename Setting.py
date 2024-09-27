from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, uic, QtGui
from threading import Thread
import time

import CreateObject




class Operation(QObject):
    update_widget = pyqtSignal(QRectF)
    game_over = pyqtSignal()
    
    
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.rect = QRectF(self.main.label.rect())
        self.isStart = False
        
        self.size = 20
        
        self.update_widget.connect(self.main.redraw)
        self.game_over.connect(self.main.gameOver)
        
        
    def gameStart(self):
        # self.x, self.y를 얻는 마우스 클릭 함수를 만들어야함
        coord = (self.x, self.y)
        sizes = QSizeF(self.size, self.size)
        self.user = CreateObject.User(QRectF(coord, sizes), QColor(0, 255, 0))
        self.isStart = True
        
        self.t = Thread(target=self.theard)
        self.t.start()
        
        
    def gameEnd(self):
        self.isStart = False
        
        
    def keyPressed(self, key):
        self.user.keyUpdate(key, True)
        
    
    def keyReleased(self, key):
        self.user.keyUpdate(key, False)
        
        
    def draw(self, painter):
        if self.isStart:
            brush = QBrush(self.user.color)
            painter.setBrush(brush)
            painter.drawRect(self.user.rect)
        else:
            print("마우스 클릭으로 x, y 값을 얻어 사각형 그리기 구현 필요")
            
            
    def update(self):
        self.update_widget.emit(self.user.rect)
    
    
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            local_pos = self.mapFromGlobal(e.globalPos())  
            self.x = local_pos.x()  
            self.y = local_pos.y()
            
            print(self.x, self.y)
        
        
    def theard(self):
        while self.isStart:
            self.user.moveUpdate()
            self.update()
            
            if self.user.isCollided:
                self.game_over.emit()
                break
            
            time.sleep(0.01)