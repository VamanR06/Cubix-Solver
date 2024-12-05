import cv2
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances

'''
This script webcam.py opens a live video feed and 
will show you a grid where 9 pixels are identified by color

IMPORTANT

PRESS q to exit
PRESS p to snapshot (print array)

GOOD LUCK TEAM!

-Ayan


'''



# Define reference Rubik's Cube colors (RGB)
rubiks_colors = {
    'White': (255, 255, 255),
    'Yellow': (255, 255, 0),
    'Red': (216, 29, 36),
    'Blue': (0, 0, 255),
    'Green': (0, 255, 0),
    'Orange': (252, 113, 37)
}

# Function to categorize a given RGB pixel by name
def get_pixel_name(pixel_color):
    pixel_color = np.array(pixel_color).reshape(1, -1)
    ref_colors = np.array(list(rubiks_colors.values()))
    distances = euclidean_distances(pixel_color, ref_colors)
    closest_index = np.argmin(distances)
    closest_color = list(rubiks_colors.keys())[closest_index]
    return closest_color

# Array where a given "side" colors are stored
color_array = []

# Open the default camera
cap = cv2.VideoCapture(0)

# Read Grid image and resize 
file_name = 'BoxRubik.png'
logo = cv2.imread(file_name) 
size = 600
logo = cv2.resize(logo, (size, size)) 
  
# Create a mask of logo 
img2gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY) 
ret, mask = cv2.threshold(img2gray, 1, 255, cv2.THRESH_BINARY) 

# Create Window
cv2.namedWindow("Live Video")

# Text info
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.75
color = (255, 255, 255) 
thickness = 2

# 9 Pixel Locations
pixel_locs = {
    (806,398),
    (953,398),
    (1095,398),
    (806,537),
    (953,537),
    (1095,537),
    (806,681),
    (953,681),
    (1095,681)
}

# Main Live Video Loop
while True:
    # Read a frame from the camera
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    
    # Get the dimensions of the frame
    frame_height, frame_width = frame.shape[:2]

    # Calculate the center coordinates
    center_y, center_x = frame_height // 2, frame_width // 2

    # Calculate the top-left corner of the ROI to center the logo
    top_left_y = center_y - size // 2
    top_left_x = center_x - size // 2

    # Define the ROI for placing the logo in the center of the frame
    roi = frame[top_left_y:top_left_y + size, top_left_x:top_left_x + size]

    # Fetch the 9 box pixel values
    for p in pixel_locs:
        pix = frame[p[1],p[0]]
        color_name =  get_pixel_name(tuple(reversed(tuple(pix))))
        color_array.append(color_name)
        text = f"{color_name}"
        cv2.putText(frame, text, p, font, font_scale, color, thickness)

    # Take photo if "P" is pressed
    if cv2.waitKey(1) == ord('p'):
        print(f'\nSNAPSHOT TAKE\n{np.reshape(color_array, (3,3))}')
    color_array = []

    # Set an index of where the mask is 
    roi[np.where(mask)] = 0
    roi += logo

    # Check if the frame was successfully read
    if not ret:
        break

    # Display the frame
    cv2.imshow('Live Video', frame)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) == ord('q'):
        break
    
   

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()



