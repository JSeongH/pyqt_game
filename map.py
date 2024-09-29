from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *




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