from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from threading import Thread
import time




class Unit():
    def __init__(self, shape=QRectF(), color=QColor()):
        self.rect = shape
        self.color = color
        
        
        
class User(Unit):
    def __init__(self, shape=QRectF(), color=QColor()):
        super().__init__(shape, color)
        # 0 : 왼, 1 : 위, 2 : 오, 3 : 아
        self.direction = [False, False, False, False]
        self.isCollided = False
        
    
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
        self.isStart = True
        
        self.t = Thread(target=self.theard)
        self.t.start()
        
        
    def gameEnd(self):
        self.isStart = False
        
        
    def keyPressed(self, key):
        self.user.keyUpdate(key, True)
        
    
    def keyReleased(self, key):
        self.user.keyUpdate(key, False)
        
        
    def draw(self, painter=QPainter()):
        if self.isStart:
            brush = QBrush(self.user.color)
            painter.setBrush(brush)
            painter.drawRect(self.user.rect)
        else:
            coord = QPointF(self.x, self.y)
            sizes = QSizeF(self.size, self.size)
            self.user = User(QRectF(coord, sizes), QColor(0, 255, 0))
            
            
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