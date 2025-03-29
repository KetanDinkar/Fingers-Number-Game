import cv2
import os  # Import os to restart the script
from utils import Finger_counter

def demostration():
    """It is the demostration of the finger counter project. 
    It aims to detect your hand then finding out the upper finger count.
    It calculates the finger count through processing hand ROI which parsed to areas with certain coordinates.
    """

    # Creating instances
    finger_counter = Finger_counter()
    cap = cv2.VideoCapture(0)

    # looping through the video frame by frame
    name_index = 0
    while (cap.isOpened()):

        # reading the captured images
        ret , frame = cap.read() # reading Frame 
        
        # checking if the frame is empty
        if not ret: break

        # Find out the finger count which is upen the hand
        drawn_image, finger_count = finger_counter.count_fingers(frame)

        # Restart logic: if 0 to 4 fingers are detected
        if 0 <= finger_count <= 4:
            cap.release()
            cv2.destroyAllWindows()
            os.execv(__file__, ["python"] + os.sys.argv)  # Restart the script

        # displaying the results
        cv2.imshow("Finger Counter", drawn_image) # showing Video 

        # taking the keyboard key
        k = cv2.waitKey(1)

        # exit condition
        if  k == ord("q"): 
            break

        # saving the images
        if k == ord("s"):
            cv2.imwrite(f"hand_counted_{name_index}.jpg", drawn_image)
            name_index += 1

    # re-allocating the sources
    cap.release()
    cv2.destroyAllWindows()
    

if __name__ == "__main__":
    demostration()