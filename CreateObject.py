from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *




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
            
            

class MapData():
    def __init__(self, label, map_path=None):
        self.label = label
        self.path = map_path
        
        self.mapClear()
    
    
    def mapClear(self):
        pixmap = QPixmap(self.label.size())
        pixmap.fill(Qt.transparent)  # 투명 배경으로 설정
        self.label.setPixmap(pixmap)
        
        
    def mapLoading(self):
        if self.path == None:
            print("맵을 불러올수 없습니다. ")
            return
        
        pixmap = QPixmap(self.path)
        scaled_pixmap = pixmap.scaled(800, 800, Qt.IgnoreAspectRatio)

        target_pixmap = self.label.pixmap()
        if target_pixmap:
            painter = QPainter(target_pixmap) 
            painter.drawPixmap(0, 0, scaled_pixmap)
            painter.end()
            self.label.setPixmap(target_pixmap)
        
    
    def mapCreation(self):
        print("구현필요")