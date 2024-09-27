from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, uic, QtGui
import sys

import CreateObject
import Setting




gui = uic.loadUiType("PyQt_Project/test.ui")[0]


class Main(QMainWindow, gui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Hello, User")
        map_path = "PyQt_Project/MapData/maze.png"
        
        self.set = Setting.Operation(self)
        

    def redraw(self, rect):
        gap = rect.width() * 0.2
        rect.adjust(-gap, -gap, gap, gap)
        self.update(rect.toAlignedRect())
        
        
    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self.label)
        self.set.draw(painter)
        painter.end()
        
        
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
    
    
    def closeEvent(self, e):
        self.set.gameEnd()
        
        
    def gameOver(self):
        print("죽어서 게임이 끝나면 어떻게 할것인가 구현 필요")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = Main()
    game.show()
    sys.exit(app.exec())
    