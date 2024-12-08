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
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances
import time


from solver import *


# Read Grid image and resize 
file_name = 'images/BoxRubik.png'
logo = cv2.imread(file_name) 
size = 600
logo = cv2.resize(logo, (size, size)) 

# Create a mask of logo 
img2gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY) 
ret, mask = cv2.threshold(img2gray, 1, 255, cv2.THRESH_BINARY) 

# Text info
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1.0
color = (255, 255, 255) 
thickness = 2



# 9 Pixel Locations
pixel_locs = [
    (806,398),
    (953,398),
    (1095,398),
    (806,537),
    (953,537),
    (1095,537),
    (806,681),
    (953,681),
    (1095,681)
]


# Define reference Rubik's Cube colors (RGB)
rubiks_colors = {
    'White': (255, 255, 255),
    'Yellow': (255, 234, 20),
    'Red': (216, 29, 36),
    'Blue': (15, 61, 219),
    'Green': (40, 208, 80),
    'Orange': (252, 113, 10)
}

colors_to_faces = {
    "orange": "U",
    "yellow": "L",
    "green": "F",
    "white": "R",
    "blue": "B",
    "red": "D"
}

# Function to categorize a given RGB pixel by name
def get_pixel_name(pixel_color):
    pixel_color = np.array(pixel_color).reshape(1, -1)
    ref_colors = np.array(list(rubiks_colors.values()))
    distances = euclidean_distances(pixel_color, ref_colors)
    closest_index = np.argmin(distances)
    closest_color = list(rubiks_colors.keys())[closest_index]
    return closest_color

def fetch_pixels(locations, frame):
    out_colors=[]
    for i, (x,y) in enumerate(locations):
        pix_out = frame[y,x]
        pixel_color_name =  get_pixel_name(tuple(reversed(tuple(pix_out))))
        out_colors.append(pixel_color_name)
        
    face = np.fliplr(np.reshape(out_colors, (3,3)))
    face = face.flatten().tolist()

    return face


class VideoThread(QThread):
    frame_signal = Signal(QImage)
    color_signal = Signal(dict)

    frame = None

    def run(self):
        self.cap = cv2.VideoCapture(0)
        
        while self.cap.isOpened():
            _, self.frame = self.cap.read()
            self.frame = cv2.flip(self.frame, 1)
            color = (255,255,255)
            expected_color = (255,255,255)
            color_array = []

            # PUT GRID
            # Get the dimensions of the frame
            frame_height, frame_width = self.frame.shape[:2]

            # Calculate the center coordinates
            center_y, center_x = frame_height // 2, frame_width // 2

            # Calculate the top-left corner of the ROI to center the logo
            top_left_y = center_y - size // 2
            top_left_x = center_x - size // 2

            # Define the ROI for placing the logo in the center of the frame
            roi = self.frame[top_left_y:top_left_y + size, top_left_x:top_left_x + size]

            # REAL-TIME Color Display
            for p in pixel_locs:
                pix = self.frame[p[1],p[0]]
                color_name =  get_pixel_name(tuple(reversed(tuple(pix))))
                color_array.append(color_name)
                if len(color_array) == 5:
                    side_color = color_name
                    if side_color == expected_color:
                        color = (0,255,0)
                    else:
                        color = (0,0,255)
                        
                text = f"{color_name}"
                cv2.putText(self.frame, text, (p[0]-45,p[1]-40), font, font_scale, color, thickness)
                # cv2.putText(frame, f"{p}", (p[0]-20,p[1]+20), font, font_scale, color, thickness)
                color = (255,255,255)
            

            # Set an index of where the mask is 
            roi[np.where(mask)] = 0
            roi += logo

            frame_label = self.cvimage_to_label(self.frame)
            self.frame_signal.emit(frame_label)

    def take_picture(self):
        cv2.putText(self.frame, f"NEW SNAPSHOT TAKEN", (10,50), font, font_scale, color, thickness)
        color_array = fetch_pixels(pixel_locs, self.frame)
        time.sleep(1)
        self.color_signal.emit({color_array[4].lower(): color_array})
        print(f'\nNEW SNAPSHOT TAKEN!')
        # sides_seen.append(side_color)
        # i+=1
        # ALL_SIDES.append(color_array)

    def cvimage_to_label(self, image):
        image = imutils.resize(image, width=560)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(
            image, image.shape[1], image.shape[0], QImage.Format.Format_RGB888
        )
        return image


class RubiksCubeApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.cube = Cube()

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

        self.camera_placeholder = QLabel("Camera")
        self.camera_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.camera_placeholder.setStyleSheet(
            "border: 2px solid #666; padding-top: 160px; padding-bottom: 160px; margin 80px; font-size: 18px;"
        )
        left_col.addWidget(self.camera_placeholder)
        left_col.addStretch(1)
        
        self.message = QLabel("Message")
        self.message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        left_col.addWidget(self.message)

        # face labels to check once images are taken

        face_layout = QHBoxLayout()

        self.face_labels = {i: QLabel(f"{i.capitalize()}: ") for i in colors_to_faces}
        for i in self.face_labels:
            self.face_labels[i].setStyleSheet("margin-bottom: 10px")
            face_layout.addWidget(self.face_labels[i])

        left_col.addLayout(face_layout)

        # button for taking images
        
        self.toggle_camera_button = QPushButton("Turn On Camera")
        self.toggle_camera_button.clicked.connect(self.toggle_camera)
        
        self.camera_buttons = QGridLayout()

        self.take_picture_button = QPushButton("Take Picture")
        self.take_picture_button.clicked.connect(self.camera_thread.take_picture)

        self.retake_button = QPushButton("Retake Picure")
        self.reset_button = QPushButton("Reset Cube")
        
        self.camera_buttons.addWidget(self.take_picture_button, 0, 0)
        self.camera_buttons.addWidget(self.retake_button, 0, 1)
        self.camera_buttons.addWidget(self.reset_button, 0, 2)

        self.camera_thread.color_signal.connect(self.pic_taken)
                
        for btn in [self.toggle_camera_button, self.take_picture_button, self.retake_button, self.reset_button]:
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
            btn.hide()

        self.toggle_camera_button.show()
        
        left_col.addLayout(self.camera_buttons)
        left_col.addWidget(self.toggle_camera_button)

        main_layout.addLayout(left_col)

        # setting up right col, 3d visualizer


        

        right_col = QVBoxLayout()

        # Create QLabel for displaying the image
        cube_image = QLabel()
        cube_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cube_image.setStyleSheet(
            "border: 2px solid #666; padding: 20px; margin: 10px;"
        )

        # Load and set the image dynamically
        image_path = "images/cubeNote.png"  # Replace this with the path to your image
        pixmap = QPixmap(image_path)
        # cube_image.setPixmap(pixmap.scaled(cube_image.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

        # Set desired size (width, height) in pixels
        image_width = 600
        image_height = 400

        # Scale the image to the specified size
        cube_image.setPixmap(pixmap.scaled(image_width, image_height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

                

        right_col.addWidget(cube_image)

        # cube_placeholder = QLabel("3D Cube Visualization Here")
        # cube_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # cube_placeholder.setStyleSheet(
        #     "border: 2px solid #666; padding: 20px; margin: 10px; font-size: 18px;"
        # )
        # right_col.addWidget(cube_placeholder)

        # solve and reset buttons

        self.solve_button = QPushButton("Solve")
        self.solve_button.setStyleSheet(
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
        
        self.solve_button.clicked.connect(lambda: self.message.setText(self.cube.solve()))

        right_col.addWidget(self.solve_button)
        main_layout.addLayout(right_col)

        central_widget.setLayout(main_layout)

    @Slot(QImage)
    def setImage(self, image):
        self.camera_placeholder.setStyleSheet(
            "border: 2px solid #666; margin 80px; font-size: 18px;"
        )
        self.camera_placeholder.setPixmap(QPixmap.fromImage(image))

    @Slot()
    def pic_taken(self, data: dict):
        self.cube.set_face(side=list(data.keys())[0], pieces=list(data.values())[0])
        self.cube.print()
        self.face_labels[list(data.keys())[0]].setText(f"{list(data.keys())[0].capitalize()}: {colors_to_faces[list(data.keys())[0]]}")
        self.message.setText("SNAPSHOT TAKEN!")

    def toggle_camera(self):
        if self.take_picture_button.isVisible():
            for btn in [self.reset_button, self.retake_button, self.take_picture_button]:
                btn.hide()

            self.toggle_camera_button.setText(f"Turn On Camera")

            self.camera_thread.quit()

        else:
            for btn in [self.reset_button, self.retake_button, self.take_picture_button]:
                btn.show()

            self.toggle_camera_button.setText(f"Turn Off Camera")
            
            self.camera_thread.start()

if __name__ == "__main__":
    app = QApplication([])
    window = RubiksCubeApp()
    window.show()
    app.exec()
