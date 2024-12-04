from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLabel,
    QGridLayout,
)
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt, QThread
from PySide6.QtCore import Signal, Slot
import cv2, imutils


class VideoThread(QThread):
    frame_signal = Signal(QImage)

    def run(self):
        self.cap = cv2.VideoCapture(0)
        while self.cap.isOpened():
            _, frame = self.cap.read()
            frame = self.cvimage_to_label(frame)
            self.frame_signal.emit(frame)

    def cvimage_to_label(self, image):
        image = imutils.resize(image, width=640)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(
            image, image.shape[1], image.shape[0], QImage.Format.Format_RGB888
        )
        return image


class RubiksCubeApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # setting up the window

        self.setWindowTitle("Cubix Solver")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #1e1e1e; color: #ffffff;")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()

        # set up the left side

        left_col = QVBoxLayout()

        # title

        title = QLabel("Rubik's Cube Solver")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; margin: 10px; padding: 5px")
        title.setFixedHeight(90)

        left_col.addWidget(title)

        # camera business

        self.camera_thread = VideoThread()
        self.camera_thread.frame_signal.connect(self.setImage)

        # placeholder for camera

        self.camera_placeholder = QLabel("camera placeholder")
        self.camera_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.camera_placeholder.setStyleSheet(
            "border: 2px solid #666; padding-top: 160px; padding-bottom: 160px; margin 80px; font-size: 18px;"
        )
        left_col.addWidget(self.camera_placeholder)
        left_col.addStretch(1)

        # face labels to check once images are taken

        face_layout = QHBoxLayout()
        face1 = QLabel("Face 1: ")
        face2 = QLabel("Face 2: ")
        face3 = QLabel("Face 3: ")
        face4 = QLabel("Face 4: ")
        face5 = QLabel("Face 5: ")
        face6 = QLabel("Face 6: ")

        for face in [face1, face2, face3, face4, face5, face6]:
            face.setStyleSheet("margin-bottom: 30px")

        face_layout.addWidget(face1)
        face_layout.addWidget(face2)
        face_layout.addWidget(face3)
        face_layout.addWidget(face4)
        face_layout.addWidget(face5)
        face_layout.addWidget(face6)

        left_col.addLayout(face_layout)

        # button for taking images

        take_picture_button = QPushButton("Take Picture")
        take_picture_button.clicked.connect(self.open_camera)
        take_picture_button.setStyleSheet(
            """
                                          QPushButton {
                                                background-color: #0078D7;
                                                border-radius: 10px;
                                                padding: 10px;
                                                color: white;
                                                font-size: 16px;
                                            }
                                            QPushButton:hover {
                                                background-color: #005FA3;
                                            }
                                            QPushButton:pressed {
                                                background-color: #004080;
                                            }
                                              """
        )
        left_col.addWidget(take_picture_button)

        main_layout.addLayout(left_col)

        # setting up right col, 3d visualizer

        right_col = QVBoxLayout()
        cube_placeholder = QLabel("3D Cube Visualization Here")
        cube_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cube_placeholder.setStyleSheet(
            "border: 2px solid #666; padding: 20px; margin: 10px; font-size: 18px;"
        )
        right_col.addWidget(cube_placeholder)

        button_layout = QGridLayout()

        # solve and reset buttons

        solve_button = QPushButton("Solve")
        reset_button = QPushButton("Reset")
        for btn in [solve_button, reset_button]:
            btn.setStyleSheet(
                """
                QPushButton {
                    background-color: #0078D7; 
                    border-radius: 10px; 
                    padding: 10px; 
                    color: white; 
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: #005FA3;
                }
                QPushButton:pressed {
                    background-color: #004080;
                }
            """
            )
        button_layout.addWidget(solve_button, 0, 0)
        button_layout.addWidget(reset_button, 0, 1)

        right_col.addLayout(button_layout)
        main_layout.addLayout(right_col)

        central_widget.setLayout(main_layout)

    @Slot(QImage)
    def setImage(self, image):
        self.camera_placeholder.setStyleSheet(
            "border: 2px solid #666; margin 80px; font-size: 18px;"
        )
        self.camera_placeholder.setPixmap(QPixmap.fromImage(image))

    def open_camera(self):
        self.camera_thread.start()


if __name__ == "__main__":
    app = QApplication([])
    window = RubiksCubeApp()
    window.show()
    app.exec()
