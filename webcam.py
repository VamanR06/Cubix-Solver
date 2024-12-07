import cv2
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances
import time

'''
This script webcam.py opens a live video feed and 
will show you a grid where 9 pixels are identified by color

IMPORTANT

PRESS q to exit
PRESS p to snapshot (print array)
PRESS r to reset (list of seen colors)

GOOD LUCK TEAM!

-Ayan


Updates (latest):

Adding instructions to screen...

1. Show cube such that white-center side faces the camera and red-center side faces down
2. Turn the cube to your left so now blue-center should face the camera
3. Turn the cube left again to show yellow-center
4. Left again for green-center
5. Turn cube up to show orange-center (top)
6. Turn cube up TWICE to show red-center (bottom)

^Same configuation in main.py


Notes:

- prints next instruction every time "p" (photo) is pressed
- print relevant arrays


'''

window_name = "Rubik's Cube"

# Define reference Rubik's Cube colors (RGB)
rubiks_colors = {
    'White': (255, 255, 255),
    'Yellow': (255, 234, 20),
    'Red': (216, 29, 36),
    'Blue': (15, 61, 219),
    'Green': (40, 208, 80),
    'Orange': (252, 113, 10)
}

# Function to categorize a given RGB pixel by name
def get_pixel_name(pixel_color):
    pixel_color = np.array(pixel_color).reshape(1, -1)
    ref_colors = np.array(list(rubiks_colors.values()))
    distances = euclidean_distances(pixel_color, ref_colors)
    closest_index = np.argmin(distances)
    closest_color = list(rubiks_colors.keys())[closest_index]
    return closest_color

# include side number

# orange side should be rotated 90, rest are ok
def fetch_pixels(locations, loop):
    out_colors=[]
    for (x,y) in locations:
        pix_out = frame[y,x]
        pixel_color_name =  get_pixel_name(tuple(reversed(tuple(pix_out))))
        out_colors.append(pixel_color_name)
        # print(f"{(x,y)} - {pix_out} - {pixel_color_name}")
    face = np.fliplr(np.rot90(np.rot90(np.reshape(out_colors, (3,3)), k=-1)))
    if loop == 4 or loop == 5:
        face = np.rot90(face, k=-1)

    face = face.flatten().tolist()

    return face

# Array where a given "side" colors are stored
color_array = []

sides_seen = []

# Open the default camera
cap = cv2.VideoCapture(0)

# Read Grid image and resize 
file_name = 'images/BoxRubik.png'
logo = cv2.imread(file_name) 
size = 600
logo = cv2.resize(logo, (size, size)) 
  
# Create a mask of logo 
img2gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY) 
ret, mask = cv2.threshold(img2gray, 1, 255, cv2.THRESH_BINARY) 

# Create Window
cv2.namedWindow(window_name)

# Text info
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.75
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

i = 0
steps = [

    "1. Show cube such that white-center side faces the camera and red-center side faces down",
    "2. Turn the cube to your left so now blue-center should face the camera",
    "3. Turn the cube left again to show yellow-center",
    "4. Left again for green-center",
    "5. Turn cube up to show orange-center (top)",
    "6. Turn cube up TWICE to show red-center (bottom)"

]

# order of side-color we're supposed to see
order = ["White", "Blue", "Yellow", "Green", "Orange", "Red"]

# FINAL
ALL_SIDES = []

# Main Live Video Loop
while True:
    # Read a frame from the camera
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    
    # Print current instruction to scree
    cv2.putText(frame, f"{steps[i]}", (10,1010), font, font_scale, color, thickness)

    # Know what side-color the user is intended to show at this point
    expected_color = order[i]

    # Get the dimensions of the frame
    frame_height, frame_width = frame.shape[:2]

    # Calculate the center coordinates
    center_y, center_x = frame_height // 2, frame_width // 2

    # Calculate the top-left corner of the ROI to center the logo
    top_left_y = center_y - size // 2
    top_left_x = center_x - size // 2

    # Define the ROI for placing the logo in the center of the frame
    roi = frame[top_left_y:top_left_y + size, top_left_x:top_left_x + size]

    # Save center color
    side_color = ""

    # Take photo if "P" is pressed
    if cv2.waitKey(1) == ord('p'):
        cv2.putText(frame, f"P PRESSED", (10,50), font, font_scale, color, thickness)
        mid_color = color_array[4]
        if mid_color in sides_seen:
            time.sleep(1)
            cv2.putText(frame, f"ALREADY SEEN", (center_x-100,1000), font, font_scale, color, thickness)
            time.sleep(1)
            print("\nNO SNAPSHOT - ALREADY SEEN!")
        elif mid_color != expected_color:
            time.sleep(1)
            cv2.putText(frame, f"WRONG SIDE", (center_x-100,150), font, font_scale, color, thickness)
            time.sleep(1)
            print("\nNO SNAPSHOT - OUT OF ORDER!")
        else:
            time.sleep(1)
            cv2.putText(frame, f"NEW SNAPSHOT TAKEN", (10,50), font, font_scale, color, thickness)
            time.sleep(1)
            color_array = fetch_pixels(pixel_locs, i)
            print(f'\nNEW SNAPSHOT TAKEN! - {mid_color} side\n{color_array}')
            sides_seen.append(side_color)
            i+=1
            ALL_SIDES.append(color_array)

            # Auto close after all sides have been seen
            if len(sides_seen) >= 6:
                break
    color_array = []

    # REAL-TIME Color Display
    for p in pixel_locs:
        pix = frame[p[1],p[0]]
        color_name =  get_pixel_name(tuple(reversed(tuple(pix))))
        color_array.append(color_name)
        if len(color_array) == 5:
            side_color = color_name
            if side_color == expected_color:
                color = (0,255,0)
            else:
                color = (0,0,255)
        text = f"{color_name}"
        cv2.putText(frame, text, (p[0]-20,p[1]), font, font_scale, color, thickness)
        cv2.putText(frame, f"{p}", (p[0]-20,p[1]+20), font, font_scale, color, thickness)
        color = (255,255,255)

    # Delete recent side (retake)
    if cv2.waitKey(1) == ord('d'):
        cv2.putText(frame, f"RESET", (10,50), font, font_scale, color, thickness)
        i-=1
        sides_seen = sides_seen[:-1]
        ALL_SIDES = ALL_SIDES[:-1]
        print("\n*DELETE LATEST SIDE*")

    # Reset what colors have been seen
    if cv2.waitKey(1) == ord('r'):
        cv2.putText(frame, f"RESET", (10,50), font, font_scale, color, thickness)
        i = 0
        sides_seen = []
        ALL_SIDES = []
        print("\n*RESET CACHE*")

    # Set an index of where the mask is 
    roi[np.where(mask)] = 0
    roi += logo

    # Check if the frame was successfully read
    if not ret:
        break
    
    # Print Controls on top of screen
    cv2.putText(frame, "HOLD Q TO QUIT", (center_x-100,50), font, font_scale, color, thickness)
    cv2.putText(frame, "PRESS P TO SNAPSHOT", (center_x-140,80), font, font_scale, color, thickness)
    cv2.putText(frame, "PRESS R TO RESET", (center_x-110,110), font, font_scale, color, thickness)
    cv2.putText(frame, "PRESS D TO DELETE", (center_x-112,140), font, font_scale, color, thickness)

    # Display the frame
    cv2.imshow(window_name, frame)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) == ord('q'):
        break
    
   

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()

print(f'\n\n{ALL_SIDES}')

