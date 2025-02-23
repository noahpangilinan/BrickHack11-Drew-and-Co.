import cv2
import mediapipe as mp
import time
import numpy as np

# List to store messages with their timestamps
active_messages = []

# Lists to track wrist positions over time
right_wrist_tracker = []
left_wrist_tracker = []

def display_text_on_feed(image):
    """
    Overlay multiple messages staggered on the same screen as the video feed.
    """
    global active_messages
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    thickness = 2
    color = (255, 255, 255)  # Red color
    line_spacing = 40  # Space between messages
    start_x = 50  # Left margin
    start_y = 50  # Top margin

    # Remove messages older than 3 seconds
    current_time = time.time()
    active_messages = [msg for msg in active_messages if current_time - msg[1] < 3]

    # Display messages staggered vertically
    for i, (text, _) in enumerate(active_messages):
        y_position = start_y + i * line_spacing
        cv2.putText(image, text, (start_x, y_position), font, font_scale, color, thickness, cv2.LINE_AA)

    return image

def display_message(string):
    """
    Add a message to be displayed.
    """
    global active_messages
    active_messages.append((string, time.time()))  # Store message with timestamp

def track_wrist(rXcord, rYcord, lXcord, lYcord):
    """
    Adds wrist coordinates to the respective trackers.
    """
    global right_wrist_tracker, left_wrist_tracker
    
    # Store wrist coordinates with timestamps
    right_wrist_tracker.append((rXcord, rYcord, time.time()))
    left_wrist_tracker.append((lXcord, lYcord, time.time()))
    
    check_wrist()

def check_wrist():
    """
    Removes old wrist coordinates and checks for movement.
    """
    global right_wrist_tracker, left_wrist_tracker
    current_time = time.time()
    
    # Remove old coordinates (older than 5 seconds)
    right_wrist_tracker = [coord for coord in right_wrist_tracker if current_time - coord[2] < 5]
    left_wrist_tracker = [coord for coord in left_wrist_tracker if current_time - coord[2] < 5]
    
    # Ensure we have at least 2 data points for movement comparison
    if len(right_wrist_tracker) < 2 or len(left_wrist_tracker) < 2:
        return
    
    # Get the latest wrist positions
    rlatest_x, rlatest_y, _ = right_wrist_tracker[-1]
    llatest_x, llatest_y, _ = left_wrist_tracker[-1]
    
    movement_threshold = 0.02  # Adjust threshold as needed
    
    # Check right wrist movement
    for x, y, _ in right_wrist_tracker[:-1]:
        if np.sqrt((rlatest_x - x) ** 2 + (rlatest_y - y) ** 2) > movement_threshold:
            return
    
    # Check left wrist movement
    for x, y, _ in left_wrist_tracker[:-1]:
        if np.sqrt((llatest_x - x) ** 2 + (llatest_y - y) ** 2) > movement_threshold:
            return
    
    print("Move your wrist")
    display_message("Move your wrist")

def body_tracker():
    """
    Tracks body movement using MediaPipe and displays text messages on the video feed.
    """
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Error: Could not open camera.")
        return
    
    last_track_time = time.time()
    
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cam.isOpened():
            ret, frame = cam.read()
            if not ret:
                print("Error: Video frame could not be read.")
                break
            
            # Convert frame to RGB for MediaPipe processing
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            
            # Process pose detection
            results = pose.process(image)
            
            # Convert frame back to BGR for OpenCV display
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Draw pose landmarks
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            
            try:
                landmarks = results.pose_landmarks.landmark
                
                # Get wrist coordinates
                right_wrist = [
                    landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                    landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y
                ]
                left_wrist = [
                    landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y
                ]
                
                # Track wrist movement every second
                if time.time() - last_track_time >= 1:
                    track_wrist(right_wrist[0], right_wrist[1], left_wrist[0], left_wrist[1])
                    last_track_time = time.time()
            
            except AttributeError:
                pass
            
            # Display messages on the video feed
            image = display_text_on_feed(image)
            
            # Show the processed frame
            cv2.imshow('MediaPipe Feed', image)
            
            # Press 'q' to exit
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
    
    cam.release()
    cv2.destroyAllWindows()
