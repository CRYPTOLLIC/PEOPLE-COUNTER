import cv2
import serial
import time

# Initialize variables
max_capacity = 1
people_count = 0
arduino=serial.Serial('COM7',9600,timeout=0.1)
def read_write(X):
    arduino.write(bytes(X, 'utf_8'))
    time.sleep(0.05)
    data=arduino.readline()
    return data
# Load pre-trained Haar Cascade classifier for detecting faces
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Ensure the Haar Cascade classifier is loaded successfully
if face_cascade.empty():
    print("Error: Unable to load Haar Cascade classifier.")
    exit()

# Start capturing video from the default camera (adjust the argument as needed)

# Open a serial connection to Arduino
#arduino = serial.Serial('COM7', 9600,timeout=0.1)  # Adjust the COM port and baud rate as needed

while True:
    cap = cv2.VideoCapture(0)

    # Read each frame from the video stream
    ret, frame = cap.read()

    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame using the Haar Cascade classifier
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    # Count the number of faces (people) present at an instance
    people_count = len(faces)

    # Display rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Display the number of persons in the frame
    cv2.putText(frame, f"People Count: {people_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    read_write(str(people_count))
    cap.release()


    # Display "Limit Exceeded" message in red when the limit is exceeded
    if people_count > max_capacity:
        cv2.putText(frame, "Limit Exceeded", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Display the processed frame in a window named 'People Counter'
    cv2.imshow('People Counter', frame)

    # Send the people count to Arduino
    #arduino.write(f"{people_count}\n".encode('utf-8'))
   

    # Delay for stability and to avoid overwhelming the serial connection
    time.sleep(0.1)

    # Break the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object, close the serial connection, and close the window
cap.release()
arduino.close()
cv2.destroyAllWindows()
