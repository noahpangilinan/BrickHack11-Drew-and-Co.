import cv2
import mediapipe as mp
import time

# List to store messages with their timestamps
active_messages = []
xRightEarCoords = []
xLeftEarCoords = []

def display_text_on_feed(image):
    """
    Overlay multiple messages staggered on the same screen as the video feed.
    """
    global active_messages
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    thickness = 2
    color = (0, 0, 255)  # Red color
    line_spacing = 40  # Space between messages
    start_x = 50  # Left margin
    start_y = 50  # Top margin

    # Filter out old messages
    current_time = time.time()
    active_messages = [msg for msg in active_messages if current_time - msg[1] < 3]  # Remove old messages after 3 seconds

    # Display messages staggered vertically
    for i, (text, timestamp) in enumerate(active_messages):
        y_position = start_y + i * line_spacing
        cv2.putText(image, text, (start_x, y_position), font, font_scale, color, thickness, cv2.LINE_AA)

    return image


def display_message(string):
    """
    Add a message to be displayed.
    """
    global active_messages
    active_messages.append((string, time.time()))  # Store message with timestamp


def body_tracker():
    """
    Tracks body movement using MediaPipe and displays text messages on the video feed.
    """
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Camera opening error")
        return

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cam.isOpened():
            ret, frame = cam.read()
            if not ret:
                print("Video has ended or cannot read the frame.")
                break

            # Convert to RGB for MediaPipe
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Process pose detection
            results = pose.process(image)

            # Convert back to BGR for OpenCV
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Draw landmarks
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            try:
                landmarks = results.pose_landmarks.landmark
                noseX = landmarks[mp_pose.PoseLandmark.NOSE.value].x
                leftEarX = landmarks[mp_pose.PoseLandmark.LEFT_EAR.value].x
                rightEarX = landmarks[mp_pose.PoseLandmark.RIGHT_EAR.value].x

                if (rightEarX > noseX):
                    xRightEarCoords.append(rightEarX)
                else:
                    xRightEarCoords.clear()

                if (leftEarX < noseX):
                    xLeftEarCoords.append(leftEarX)
                else:
                    xLeftEarCoords.clear()

                if (len(xRightEarCoords) > 35 or len(xLeftEarCoords) > 35):
                    display_message("TURN HEAD")
                    
            except Exception as e:
                pass

            # Display messages
            image = display_text_on_feed(image)

            # Show the modified frame
            cv2.imshow('Mediapipe Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    cam.release()
    cv2.destroyAllWindows()

