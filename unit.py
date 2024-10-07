import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage, QPixmap

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage)

    def __init__(self, video_source):
        super().__init__()
        self.video_source = video_source
        self.running = True

    def run(self):
        cap = cv2.VideoCapture(self.video_source)
        while self.running:
            ret, frame = cap.read()
            if ret:
                # BGR to RGB
                
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                self.change_pixmap_signal.emit(convert_to_Qt_format)
            else:
                break  # 프레임을 더 이상 읽을 수 없으면 루프 종료

        cap.release()

    def stop(self):
        self.running = False
        self.quit()
        self.wait()


class VideoPlayer(QMainWindow):
    def __init__(self, video_source):
        super().__init__()
        self.setWindowTitle("Video Player")
        
        # QLabel 생성
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        
        # 버튼 생성
        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.start_video)
        
        self.stop_button = QPushButton("Stop", self)
        self.stop_button.clicked.connect(self.stop_video)

        # 레이아웃 설정
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # 비디오 스레드 초기화
        self.video_thread = VideoThread(video_source)
        self.video_thread.change_pixmap_signal.connect(self.update_image)

    def start_video(self):
        self.video_thread.start()
        print(self.video_thread.running)

    def stop_video(self):
        self.video_thread.stop()

    def update_image(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # 비디오 파일 경로를 여기에 입력하세요
    video_path = "20241007_175402.avi"  
    player = VideoPlayer(video_path)
    player.show()
    
    sys.exit(app.exec_())
