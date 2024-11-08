import cv2

# take photo
webcam = cv2.VideoCapture(0)
contador = 0 
while True:
    check, frame = webcam.read()
    cv2.imshow("Captura", frame)
    key = cv2.waitKey(1)
    if contador==15:                     #Low contador means low light
        cv2.imwrite(filename='image.png', img=frame)
        break
    contador=contador+1
    print(contador)
webcam.release()
cv2.destroyAllWindows()




