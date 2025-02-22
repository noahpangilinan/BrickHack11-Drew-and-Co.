import cv2
import mediapipe as mp
import numpy as np      #helps with trig
#import pandas as pd  #works with the csv data


def body_tracker():
    #this is the function that will be called by the main function
    #it will return the x,y,z coordinates of the body parts
    mp_drawing = mp.solutions.drawing_utils     #gives drawing utilitys to visualize poses
    mp_pose = mp.solutions.pose     #imports pose estemation model

    cam = cv2.VideoCapture(0)       #grabing video capture divice, 0 is the number representing the webcam or first camera "filename.mp4" means video file
    if (cam.isOpened()== False):
        print("camera opening error")
        exit()


    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose: #sets up new instance of mediapip feed, inc conf or tracking to get better estimation

        while cam.isOpened():       #loops through feed by each frame
            ret, frame = cam.read()        #gives current feed from webcam ret = return variable, frame = current fram from feed
            if not ret:
                print("Video has ended or cannot read the frame.")
                break

            #recoloring image from rgb to bgr bc opencv reads images in bgr
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False #saves memery wen passed to pose esimation model

            #acceses pose model pose stores detections into results (array)
            results = pose.process(image)
            
            #revert back to rgb
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


            #drawing detections to onto image, landmarks are coordinates of points, connection is which re connected
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            cv2.imshow('Mediapipe Feed', image)     #gives popup on screen visualizing image

            if cv2.waitKey(10) & 0xFF == ord('q'):      #if q hit loop breaks
                break
